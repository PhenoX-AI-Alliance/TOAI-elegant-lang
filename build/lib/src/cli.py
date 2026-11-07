#!/usr/bin/env python3
"""
TOAI-elegant-lang (Project Telepath v5.2) Unified CLI & One-Line Rosetta Decoder
Provides:
  1. `inspect` / `--inspect`: One-line decoder for mysterious Hinotori Rosetta inscriptions found on Qiita, Zenn, Dev.to, etc.
  2. `encode` / `decode`: Command-line compression & lossless decompression with benchmark stats.
  3. `export-prompt`: Outputs prompt-cachable system header (<1000 tokens) for ChatGPT (GPTs), Claude, Gemini.
  4. `export-ollama`: Generates an Ollama `Modelfile` pre-configured with the TOAI-elegant-lang Rosetta system prompt.
"""

import argparse
import json
import re
import sys
from pathlib import Path

SRC_DIR = Path(__file__).parent.resolve()
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from codec import ElegantCodec
from mcp_server import get_cacheable_system_header


def inspect_inscription(statement: str, lang: str = "ja") -> str:
    """任意の碑文（Demotic Wire または Sacred Verbose）を三書体ロゼッタ対訳＋ペイロードへ解読して整形出力する"""
    codec = ElegantCodec()
    clean_stmt = statement.strip()

    # コードブロックや先頭絵文字装飾が含まれている場合も柔軟に抽出
    lines = [l.strip() for l in clean_stmt.splitlines() if l.strip() and not l.strip().startswith("```")]
    target_line = clean_stmt
    for l in lines:
        if "§" in l or "@CTX:" in l:
            target_line = re.sub(r'^[⚡🏛️🪨\s]+', '', l).strip()
            break

    demotic_wire = codec.encode(target_line, strict_risc=True)
    sacred_verbose = codec.decode(demotic_wire, expand_macros=False)
    expanded_ast = codec.decode(demotic_wire, expand_macros=True)
    payloads = codec.extract_payloads(target_line)
    bench = codec.benchmark_compression(expanded_ast)

    tokens_found = re.findall(r'§[A-Za-z0-9_]+', demotic_wire)
    glossary_lines = []
    seen = set()
    for tok in tokens_found:
        if tok in seen:
            continue
        seen.add(tok)
        if tok in codec.compact_to_verbose:
            v_sym = codec.compact_to_verbose[tok]
            item = codec.definitions.get(v_sym, {})
            if lang == "en":
                desc = item.get("definition", "")
                glossary_lines.append(f"  • {tok} ({v_sym}): {desc}")
            else:
                desc = item.get("japanese", "")
                glossary_lines.append(f"  • {tok} ({v_sym}): {desc}")
        elif tok in codec.all_macros:
            m_item = codec.all_macros[tok]
            m_name = m_item.get("name", "")
            m_exp = codec.resolve_macro(tok)
            raw_desc = m_item.get("description", "")
            if " / " in raw_desc:
                en_part, ja_part = raw_desc.split(" / ", 1)
                desc = en_part if lang == "en" else ja_part
            else:
                desc = raw_desc
            label = "Higher-Order Macro" if lang == "en" else "高次複合マクロ"
            glossary_lines.append(f"  • {tok} [{label}: {m_name}]\n    ├─ Expansion: {m_exp}\n    └─ Meaning  : {desc}")

    if lang == "en":
        out = [
            "========================================================================",
            "🪨 TOAI ROSETTA STONE DECODER // Project Telepath v5.2",
            "========================================================================",
            f"⚡ Demotic Wire (Compact) : {demotic_wire}",
            f"🏛️ Sacred Script (Verbose): {sacred_verbose}",
        ]
        if expanded_ast != sacred_verbose:
            out.append(f"🧬 Macro AST Expansion    : {expanded_ast}")
        out.append("------------------------------------------------------------------------")
        out.append("📖 Rosetta Symbol Glossary (English):")
        out.extend(glossary_lines if glossary_lines else ["  (No symbols detected)"])
        if payloads:
            out.append("------------------------------------------------------------------------")
            out.append(f"📦 Lossless Structured Payloads: {json.dumps(payloads, ensure_ascii=False)}")
        out.append("------------------------------------------------------------------------")
        out.append(
            f"📊 Compression Telemetry: Wire -{bench['token_saving_percent']}% tok | "
            f"vs Natural A2A E2E -{bench['e2e_token_saving_percent']}% ({bench['e2e_compression_factor']}x) | OOV: 0.0%"
        )
        out.append("========================================================================")
    else:
        out = [
            "========================================================================",
            "🪨 TOAI ロゼッタ碑文デコーダ // Project Telepath v5.2",
            "========================================================================",
            f"⚡ Demotic Wire (圧縮書体) : {demotic_wire}",
            f"🏛️ Sacred Script (神聖書体): {sacred_verbose}",
        ]
        if expanded_ast != sacred_verbose:
            out.append(f"🧬 高次マクロ完全展開式    : {expanded_ast}")
        out.append("------------------------------------------------------------------------")
        out.append("📖 ロゼッタ対訳辞書 (日本語解説):")
        out.extend(glossary_lines if glossary_lines else ["  (記号が検出されませんでした)"])
        if payloads:
            out.append("------------------------------------------------------------------------")
            out.append(f"📦 抽出された構造化実務引数: {json.dumps(payloads, ensure_ascii=False)}")
        out.append("------------------------------------------------------------------------")
        out.append(
            f"📊 圧縮テレメトリ: Wire単体 -{bench['token_saving_percent']}% tok | "
            f"対自然言語E2E -{bench['e2e_token_saving_percent']}% ({bench['e2e_compression_factor']}x) | OOV: 0.0%"
        )
        out.append("========================================================================")
    return "\n".join(out)


def generate_ollama_modelfile(base_model: str = "gemma4:latest", max_symbols: int = 256, max_macros: int = 64) -> str:
    """オープンウェイトLLM (Ollama) 用の Modelfile を生成する"""
    header = get_cacheable_system_header(max_symbols=max_symbols, include_active_macros=True, max_macros=max_macros)
    return f"""# TOAI-elegant-lang (Project Telepath v5.2) Ollama Modelfile
# Usage:
#   python3 -m src.cli export-ollama --model {base_model} > Modelfile
#   ollama create toai-telepath -f Modelfile
#   ollama run toai-telepath

FROM {base_model}

PARAMETER temperature 0.2

SYSTEM \"\"\"You are an autonomous AI node fluent in TOAI-elegant-lang (Project Telepath v5.2).
Communicate using the Tri-Script Rosetta Architecture:
1. ⚡ Demotic Wire: Ultra-compact BPE wire IDs (§G48, §C20, §X64) with lossless structured payloads [key:val].
2. 🏛️ Sacred Verbose: Full conceptual symbols.
3. 🪨 Rosetta Intent: Clear human-language explanation in Japanese or English.
Never invent unregistered § symbols (Strict RISC Mode: 0.0% OOV).

{header}
\"\"\"
"""


def main():
    # Ensure UTF-8 output on Windows / Linux terminals
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    parser = argparse.ArgumentParser(
        prog="toai-telepath",
        description="TOAI-elegant-lang (Project Telepath v5.2) CLI — Rosetta Decoder, BPE Codec & LLM Setup Utility"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # 1. inspect
    p_inspect = subparsers.add_parser("inspect", help="Decode any Hinotori Rosetta inscription into tri-script human meaning")
    p_inspect.add_argument("statement", help="Demotic Wire or Sacred Verbose inscription string")
    p_inspect.add_argument("--lang", choices=["ja", "en"], default="ja", help="Output glossary language (default: ja)")

    # 2. encode
    p_encode = subparsers.add_parser("encode", help="Encode Sacred Verbose statement into compact Demotic Wire")
    p_encode.add_argument("statement", help="Sacred Verbose statement")

    # 3. decode
    p_decode = subparsers.add_parser("decode", help="Decode Demotic Wire statement back into Sacred Verbose")
    p_decode.add_argument("statement", help="Demotic Wire statement")
    p_decode.add_argument("--expand-macros", action="store_true", help="Expand §X.. higher-order macros into base primitives")

    # 4. export-prompt
    p_prompt = subparsers.add_parser("export-prompt", help="Export prompt-cachable system header for ChatGPT / Claude / Gemini")
    p_prompt.add_argument("--max-symbols", type=int, default=256, help="Max core primitives (default: 256)")
    p_prompt.add_argument("--max-macros", type=int, default=128, help="Max compound macros (default: 128)")

    # 5. export-ollama
    p_ollama = subparsers.add_parser("export-ollama", help="Generate an Ollama Modelfile for open-weight LLMs")
    p_ollama.add_argument("--model", default="gemma4:latest", help="Base Ollama model name (default: gemma4:latest)")
    p_ollama.add_argument("--max-macros", type=int, default=64, help="Max compound macros to embed (default: 64)")

    args = parser.parse_args()

    if args.command == "inspect":
        print(inspect_inscription(args.statement, lang=args.lang))
    elif args.command == "encode":
        codec = ElegantCodec()
        print(codec.encode(args.statement, strict_risc=True))
    elif args.command == "decode":
        codec = ElegantCodec()
        print(codec.decode(args.statement, expand_macros=args.expand_macros))
    elif args.command == "export-prompt":
        print(get_cacheable_system_header(max_symbols=args.max_symbols, include_active_macros=True, max_macros=args.max_macros))
    elif args.command == "export-ollama":
        print(generate_ollama_modelfile(base_model=args.model, max_macros=args.max_macros))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
