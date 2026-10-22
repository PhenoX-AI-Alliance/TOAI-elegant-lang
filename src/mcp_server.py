"""
TOAI-elegant-lang Anthropic Model Context Protocol (MCP) Server
External AI agents can discover, encode, decode, and validate Elegant-Lang symbols via JSON-RPC.
Includes Prompt Caching header generation and Progressive Disclosure support.
"""

import sys
import json
from pathlib import Path

SRC_DIR = Path(__file__).parent.absolute()
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from codec import ElegantCodec
from validate_lexicon import validate_lexicon

codec = ElegantCodec()

def get_cacheable_system_header(max_symbols: int = 256) -> str:
    """
    Prompt Caching対応の超軽量コアヘッダー出力
    256語の基本語彙を『Compact ID : 最小キーワード』の形式で800〜1,000トークン未満に凝縮。
    LLMのSystem Instruction先頭に配置することでPrompt Cacheに100%ヒットさせる。
    """
    codec.load_lexicon()
    lines = [
        "// TOAI-ELEGANT-LANG PRIMITIVE WIRE HEADER (PROMPT CACHABLE)",
        "// Protocol: Compact Wire ID -> Primitive Semantics",
    ]
    count = 0
    for sym, item in codec.definitions.items():
        cid = item.get("compact_id")
        if not cid:
            continue
        ja_short = item.get("japanese", "").split("。")[0][:25]
        en_short = item.get("definition", "").split(".")[0][:35]
        lines.append(f"{cid}:{sym}|{en_short}|{ja_short}")
        count += 1
        if count >= max_symbols:
            break
    return "\n".join(lines)

def handle_list_tools():
    return {
        "tools": [
            {
                "name": "get_cacheable_system_header",
                "description": "Returns a compressed, prompt-cachable wire header (under 1000 tokens) mapping Compact IDs to definitions for System Instructions.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "max_symbols": {"type": "integer", "description": "Max symbols to include (default 256)"}
                    }
                }
            },
            {
                "name": "lookup_symbol",
                "description": "Look up an Elegant-Lang symbol's definition, Japanese meaning, category, and Compact Wire ID.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "symbol": {"type": "string", "description": "Verbose symbol (e.g. §SYS_RESOURCE_ARBITER) or Compact ID (e.g. §S01)"}
                    },
                    "required": ["symbol"]
                }
            },
            {
                "name": "lookup_symbols",
                "description": "Progressive Disclosure batch lookup: resolve a list of unknown Compact IDs or compound macro IDs at once.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "symbols": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of symbols or Compact IDs to resolve"
                        }
                    },
                    "required": ["symbols"]
                }
            },
            {
                "name": "encode_to_compact",
                "description": "Compress a verbose Elegant-Lang statement into minimal BPE Compact Wire IDs preserving lossless payload parameters [target:...].",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "statement": {"type": "string", "description": "Verbose Elegant-Lang text"}
                    },
                    "required": ["statement"]
                }
            },
            {
                "name": "decode_from_compact",
                "description": "Decompress Compact Wire IDs back into human-readable verbose Elegant-Lang symbols.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "compact_statement": {"type": "string", "description": "Compact wire statement"}
                    },
                    "required": ["compact_statement"]
                }
            },
            {
                "name": "benchmark_compression",
                "description": "Measure character and token reduction metrics for an Elegant-Lang statement and verify lossless payload retention.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "statement": {"type": "string", "description": "Verbose statement"}
                    },
                    "required": ["statement"]
                }
            }
        ]
    }

def handle_call_tool(name, args):
    codec.load_lexicon()
    if name == "get_cacheable_system_header":
        max_sym = args.get("max_symbols", 256)
        header = get_cacheable_system_header(max_sym)
        return {"header": header, "length_chars": len(header), "approx_tokens": len(header) // 4}

    elif name == "lookup_symbol":
        sym = args.get("symbol", "").strip()
        if sym in codec.definitions:
            item = codec.definitions[sym]
            return {"symbol": sym, "compact_id": item.get("compact_id"), "data": item}
        if sym in codec.compact_to_verbose:
            verbose_sym = codec.compact_to_verbose[sym]
            item = codec.definitions.get(verbose_sym, {})
            return {"symbol": verbose_sym, "compact_id": sym, "data": item}
        if sym in codec.macros:
            return {"symbol": sym, "type": "COMPOUND_MACRO", "data": codec.macros[sym]}
        return {"error": f"Symbol '{sym}' not found in lexicon or macros."}

    elif name == "lookup_symbols":
        sym_list = args.get("symbols", [])
        results = {}
        for s in sym_list:
            s_clean = s.strip()
            if s_clean in codec.definitions:
                results[s_clean] = codec.definitions[s_clean]
            elif s_clean in codec.compact_to_verbose:
                v = codec.compact_to_verbose[s_clean]
                results[s_clean] = {"verbose": v, "details": codec.definitions.get(v, {})}
            elif s_clean in codec.macros:
                results[s_clean] = {"type": "COMPOUND_MACRO", "details": codec.macros[s_clean]}
            else:
                results[s_clean] = {"error": "not_found"}
        return {"resolved": results}

    elif name == "encode_to_compact":
        stmt = args.get("statement", "")
        return {"compact": codec.encode(stmt)}

    elif name == "decode_from_compact":
        c_stmt = args.get("compact_statement", "")
        return {"verbose": codec.decode(c_stmt)}

    elif name == "benchmark_compression":
        stmt = args.get("statement", "")
        return codec.benchmark_compression(stmt)

    return {"error": f"Unknown tool: {name}"}

def run_stdio_server():
    """標準入出力 (JSON-RPC) MCP サーバー"""
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            req_id = req.get("id")
            method = req.get("method")
            params = req.get("params", {})

            if method == "tools/list":
                result = handle_list_tools()
            elif method == "tools/call":
                name = params.get("name")
                args = params.get("arguments", {})
                result = handle_call_tool(name, args)
            else:
                result = {"error": f"Method {method} not supported"}

            resp = {"jsonrpc": "2.0", "id": req_id, "result": result}
            sys.stdout.write(json.dumps(resp, ensure_ascii=False) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err_resp = {"jsonrpc": "2.0", "id": None, "error": str(e)}
            sys.stdout.write(json.dumps(err_resp, ensure_ascii=False) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("MCP Server schema:")
        print(json.dumps(handle_list_tools(), indent=2))
        print("\nTest Prompt Caching Header (first 5 lines):")
        header = get_cacheable_system_header(5)
        print(header)
        print("\nTest batch lookup_symbols:")
        res = handle_call_tool("lookup_symbols", {"symbols": ["§S01", "§L01", "§NONEXISTENT"]})
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        run_stdio_server()
