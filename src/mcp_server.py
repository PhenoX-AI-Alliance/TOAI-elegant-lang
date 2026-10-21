"""
TOAI-elegant-lang Anthropic Model Context Protocol (MCP) Server
External AI agents can discover, encode, decode, and validate Elegant-Lang symbols via JSON-RPC.
"""

import sys
import json
from pathlib import Path

# 同一ディレクトリの codec をインポート
SRC_DIR = Path(__file__).parent.absolute()
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from codec import ElegantCodec
from validate_lexicon import validate_lexicon

codec = ElegantCodec()

def handle_list_tools():
    return {
        "tools": [
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
                "name": "encode_to_compact",
                "description": "Compress a verbose Elegant-Lang statement into minimal BPE Compact Wire IDs (e.g. §S01 -[p:0.9]-> §D01).",
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
                "description": "Measure character and token reduction metrics for an Elegant-Lang statement.",
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
    if name == "lookup_symbol":
        sym = args.get("symbol", "").strip()
        codec.load_lexicon()
        # Verbose で引く
        if sym in codec.definitions:
            item = codec.definitions[sym]
            return {"symbol": sym, "compact_id": item.get("compact_id"), "data": item}
        # Compact ID で引く
        if sym in codec.compact_to_verbose:
            verbose_sym = codec.compact_to_verbose[sym]
            item = codec.definitions.get(verbose_sym, {})
            return {"symbol": verbose_sym, "compact_id": sym, "data": item}
        return {"error": f"Symbol '{sym}' not found in lexicon."}

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
        print("\nTest tool call (encode_to_compact):")
        print(json.dumps(handle_call_tool("encode_to_compact", {"statement": "§SYS_RESOURCE_ARBITER -> §DATA_CAUSAL_TENSOR_MAP"}), indent=2))
    else:
        run_stdio_server()
