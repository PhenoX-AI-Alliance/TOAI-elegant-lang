#!/usr/bin/env python3
"""
TOAI-elegant-lang v5.4.3 Fair Multi-Format Benchmark & Header Amortization Suite
Compares 5 wire representations across identical multi-agent scenarios:
  1. Verbose A2A (Baseline)   : Natural language prose intent + semantic specs + standard JSON
  2. Structured Tool JSON     : Lossless structured JSON preserving intent, params, causal [p,c], and fallbacks
  3. Minified Key JSON        : Short-key minified JSON ({"c":"FX","s":[...]}) preserving control graph
  4. Simplified Template      : Minimal flat key=value template (lossy: no causal graph or fallback AST)
  5. TOAI Demotic Wire        : @CTX:... :: §ID [params] -[p,c]-> §ID => §ID (lossless + causal AST)

Also computes the Session Break-Even Point (number of messages required to amortize a ~1,000-token
system dictionary header) under both Standard (Uncached) and Prompt Caching (90% discount) regimes.
"""

import json
import math
import sys
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from codec import ElegantCodec, count_bpe_tokens


def measure_all_tokenizers(text: str) -> Dict[str, Any]:
    """
    Measure token counts using `o200k_base` and `cl100k_base` via `tiktoken` if installed,
    or deterministic BPE subword estimation (`is_estimated=True`) when offline/uninstalled.
    """
    o200k = count_bpe_tokens(text, "o200k_base")
    cl100k = count_bpe_tokens(text, "cl100k_base")
    return {
        "chars": len(text),
        "o200k_tokens": o200k["tokens"],
        "cl100k_tokens": cl100k["tokens"],
        "is_estimated": o200k["is_estimated"] or cl100k["is_estimated"],
        "encoding_label": (
            "tiktoken (o200k_base / cl100k_base)"
            if not o200k["is_estimated"]
            else "Fallback BPE Subword Estimator (is_estimated=True)"
        ),
    }


def build_scenarios(codec: ElegantCodec) -> List[Dict[str, Any]]:
    """Construct 5 representative multi-agent coordination scenarios across all 5 formats."""
    scenarios = [
        {
            "id": "S1_FX_HEDGE",
            "title": "Cooperative FX Risk Hedge & Resource Arbitrage",
            "sacred_verbose": (
                '@CTX:FX_HEDGE :: §X64 [pair:"USD/JPY", stop:150.5, mode:"cooperative"] '
                '-[p:0.99, c:0.01]-> §PROTO_HEALTH_ATTEST => §GENTLE_RESOURCE_SHARING'
            ),
            "verbose_a2a": json.dumps({
                "protocol": "STANDARD_NATURAL_LANGUAGE_A2A_JSON",
                "context": "FX_HEDGE",
                "human_intent": (
                    "Execute a cooperative foreign exchange risk hedge on USD/JPY with a stop-loss at 150.5, "
                    "throttling compute arbitrage under bounded constraints (p=0.99, cost=0.01), "
                    "followed by runtime health attestation and gentle cross-node resource sharing."
                ),
                "semantic_specifications": [
                    "GAIA_WARMTH_ARBITRAGE_FALLBACK: Negotiate mutual trust and resource allocation under bounded constraints with load fallback.",
                    "PROTO_HEALTH_ATTEST: Signed telemetry report certifying syntax validity, zero duplicates, and runtime readiness.",
                    "GENTLE_RESOURCE_SHARING: Cooperative multi-agent compute and quota sharing protocol."
                ],
                "causal_graph": {
                    "root": "GAIA_WARMTH_ARBITRAGE_FALLBACK",
                    "parameters": {"pair": "USD/JPY", "stop": 150.5, "mode": "cooperative"},
                    "transition": {"probability": 0.99, "cost": 0.01, "next": "PROTO_HEALTH_ATTEST"},
                    "consequence": "GENTLE_RESOURCE_SHARING"
                }
            }, ensure_ascii=False),
            "structured_tool_json": json.dumps({
                "context": "FX_HEDGE",
                "pipeline": [
                    {
                        "action": "GAIA_WARMTH_ARBITRAGE_FALLBACK",
                        "params": {"pair": "USD/JPY", "stop": 150.5, "mode": "cooperative"},
                        "transition": {"p": 0.99, "c": 0.01}
                    },
                    {"action": "PROTO_HEALTH_ATTEST"},
                    {"action": "GENTLE_RESOURCE_SHARING", "role": "consequence"}
                ]
            }, separators=(",", ":")),
            "minified_key_json": json.dumps({
                "c": "FX_HEDGE",
                "s": [
                    {"a": "X64", "p": {"pair": "USD/JPY", "stop": 150.5, "mode": "cooperative"}, "t": [0.99, 0.01]},
                    {"a": "G48"},
                    {"a": "C20"}
                ]
            }, separators=(",", ":")),
            "simplified_template": "FX_HEDGE|pair=USD/JPY,stop=150.5,mode=cooperative",
        },
        {
            "id": "S2_DIST_RECOVERY",
            "title": "Distributed Cluster Degraded Drain & Safe Fallback",
            "sacred_verbose": (
                '@CTX:DISTRIBUTED_RECOVERY :: §X354 [status:"degraded", threshold:0.85] '
                '-[p:0.99, c:0.01]-> §PROTO_GRACEFUL_DRAIN [action:"quiesce", timeout:15.0] '
                '!-> §PROTO_PARTIAL_COMMIT [partition:"edge-nodes"] '
                '? §SAFE_FALLBACK_HARMONY [mode:"safe"]'
            ),
            "verbose_a2a": json.dumps({
                "protocol": "STANDARD_NATURAL_LANGUAGE_A2A_JSON",
                "context": "DISTRIBUTED_RECOVERY",
                "human_intent": (
                    "Upon detecting degraded cluster health above threshold 0.85, initiate graceful node drain "
                    "(quiesce within 15.0s, p=0.99, cost=0.01), enforce partial commit on edge-nodes, "
                    "or transition into safe fallback harmony mode if recovery fails."
                ),
                "semantic_specifications": [
                    "Compound recovery macro §X354 for distributed state stabilization.",
                    "PROTO_GRACEFUL_DRAIN: Drain in-flight requests before node isolation.",
                    "PROTO_PARTIAL_COMMIT: Commit validated sub-transactions on surviving partitions.",
                    "SAFE_FALLBACK_HARMONY: Enter non-destructive safe mode preserving state invariants."
                ],
                "causal_graph": {
                    "trigger": {"symbol": "X354", "status": "degraded", "threshold": 0.85},
                    "transition": {"probability": 0.99, "cost": 0.01},
                    "primary_step": {"symbol": "PROTO_GRACEFUL_DRAIN", "action": "quiesce", "timeout": 15.0},
                    "guarded_step": {"symbol": "PROTO_PARTIAL_COMMIT", "partition": "edge-nodes"},
                    "fallback": {"symbol": "SAFE_FALLBACK_HARMONY", "mode": "safe"}
                }
            }, ensure_ascii=False),
            "structured_tool_json": json.dumps({
                "context": "DISTRIBUTED_RECOVERY",
                "trigger": {"op": "X354", "params": {"status": "degraded", "threshold": 0.85}},
                "transition": {"p": 0.99, "c": 0.01},
                "primary": {"op": "PROTO_GRACEFUL_DRAIN", "params": {"action": "quiesce", "timeout": 15.0}},
                "guarded": {"op": "PROTO_PARTIAL_COMMIT", "params": {"partition": "edge-nodes"}},
                "fallback": {"op": "SAFE_FALLBACK_HARMONY", "params": {"mode": "safe"}}
            }, separators=(",", ":")),
            "minified_key_json": json.dumps({
                "c": "DISTRIBUTED_RECOVERY",
                "s": [
                    {"a": "X354", "p": {"status": "degraded", "threshold": 0.85}, "t": [0.99, 0.01]},
                    {"a": "G19", "p": {"action": "quiesce", "timeout": 15.0}},
                    {"a": "G22", "p": {"partition": "edge-nodes"}},
                    {"fb": "H03", "p": {"mode": "safe"}}
                ]
            }, separators=(",", ":")),
            "simplified_template": "DISTRIBUTED_RECOVERY|status=degraded,threshold=0.85,action=quiesce,timeout=15.0,partition=edge-nodes,mode=safe",
        },
        {
            "id": "S3_TENSOR_ARBITRAGE",
            "title": "System Resource Arbitration & Deductive Convergence",
            "sacred_verbose": (
                '@CTX:FINANCIAL_TRADING :: §SYS_RESOURCE_ARBITER '
                '[target:"USD/JPY", limit:150.5, action:"HOLD", code:"007", p:0.98] '
                '-[cost:0.02]-> §DATA_CAUSAL_TENSOR_MAP => §LOGIC_DEDUCTIVE_CONVERGENCE'
            ),
            "verbose_a2a": json.dumps({
                "protocol": "STANDARD_NATURAL_LANGUAGE_A2A_JSON",
                "context": "FINANCIAL_TRADING",
                "human_intent": (
                    "Arbitrate system compute resources for financial trading on target USD/JPY at limit 150.5 "
                    "with HOLD action and strategy code '007' (confidence 0.98, transition cost 0.02), "
                    "projecting causal tensor map to reach deductive logical convergence."
                ),
                "semantic_specifications": [
                    "SYS_RESOURCE_ARBITER: Dynamic allocation and arbitration of system compute and memory resources.",
                    "DATA_CAUSAL_TENSOR_MAP: Multi-dimensional tensor representation of causal dependencies.",
                    "LOGIC_DEDUCTIVE_CONVERGENCE: Deterministic multi-step deductive reasoning convergence."
                ],
                "structured_parameters": [
                    {"target": "USD/JPY", "limit": 150.5, "action": "HOLD", "code": "007", "p": 0.98},
                    {"cost": 0.02}
                ]
            }, ensure_ascii=False),
            "structured_tool_json": json.dumps({
                "context": "FINANCIAL_TRADING",
                "steps": [
                    {
                        "op": "SYS_RESOURCE_ARBITER",
                        "params": {"target": "USD/JPY", "limit": 150.5, "action": "HOLD", "code": "007", "p": 0.98},
                        "edge": {"cost": 0.02}
                    },
                    {"op": "DATA_CAUSAL_TENSOR_MAP"},
                    {"op": "LOGIC_DEDUCTIVE_CONVERGENCE", "type": "convergence"}
                ]
            }, separators=(",", ":")),
            "minified_key_json": json.dumps({
                "c": "FINANCIAL_TRADING",
                "s": [
                    {"a": "S01", "p": {"target": "USD/JPY", "limit": 150.5, "action": "HOLD", "code": "007", "p": 0.98}, "e": {"cost": 0.02}},
                    {"a": "D01"},
                    {"a": "L01"}
                ]
            }, separators=(",", ":")),
            "simplified_template": "FINANCIAL_TRADING|target=USD/JPY,limit=150.5,action=HOLD,code=007,p=0.98,cost=0.02",
        },
        {
            "id": "S4_PUB_SEAL_AUDIT",
            "title": "Publication Governance Seal & Telemetry Attestation",
            "sacred_verbose": (
                '@CTX:PUB_SEAL :: §X64 [node:"TOAI7", target:"devto", note:"a, b"] '
                '-[p:0.99, c:0.01]-> §PROTO_HEALTH_ATTEST => §GENTLE_RESOURCE_SHARING [status:"harmonized"]'
            ),
            "verbose_a2a": json.dumps({
                "protocol": "STANDARD_NATURAL_LANGUAGE_A2A_JSON",
                "context": "PUB_SEAL",
                "human_intent": (
                    "Attach audited Rosetta publication seal from node TOAI7 targeting devto with note 'a, b' "
                    "(p=0.99, cost=0.01), certifying protocol health attestation and transitioning to "
                    "harmonized gentle resource sharing."
                ),
                "semantic_specifications": [
                    "GAIA_WARMTH_ARBITRAGE_FALLBACK: Bounded trust and compute throttling macro.",
                    "PROTO_HEALTH_ATTEST: Signed runtime health and syntax attestation.",
                    "GENTLE_RESOURCE_SHARING: Harmonized resource sharing across autonomous guild nodes."
                ],
                "structured_parameters": [
                    {"node": "TOAI7", "target": "devto", "note": "a, b"},
                    {"p": 0.99, "c": 0.01},
                    {"status": "harmonized"}
                ]
            }, ensure_ascii=False),
            "structured_tool_json": json.dumps({
                "context": "PUB_SEAL",
                "steps": [
                    {
                        "op": "GAIA_WARMTH_ARBITRAGE_FALLBACK",
                        "params": {"node": "TOAI7", "target": "devto", "note": "a, b"},
                        "transition": {"p": 0.99, "c": 0.01}
                    },
                    {"op": "PROTO_HEALTH_ATTEST"},
                    {"op": "GENTLE_RESOURCE_SHARING", "params": {"status": "harmonized"}}
                ]
            }, separators=(",", ":")),
            "minified_key_json": json.dumps({
                "c": "PUB_SEAL",
                "s": [
                    {"a": "X64", "p": {"node": "TOAI7", "target": "devto", "note": "a, b"}, "t": [0.99, 0.01]},
                    {"a": "G48"},
                    {"a": "C20", "p": {"status": "harmonized"}}
                ]
            }, separators=(",", ":")),
            "simplified_template": "PUB_SEAL|node=TOAI7,target=devto,note=a, b,status=harmonized",
        },
    ]

    for sc in scenarios:
        sc["toai_demotic_wire"] = str(codec.encode(sc["sacred_verbose"], on_oov="error"))
    return scenarios


SCENARIOS: List[Dict[str, Any]] = build_scenarios(ElegantCodec())


def compute_breakeven_messages(header_tokens: float, baseline_avg: float, wire_avg: float) -> Dict[str, Any]:
    """
    Calculate how many messages are required for TOAI Demotic Wire + System Header
    to break even against a given baseline format:
      - Uncached: full header cost incurred once at session start (H = header_tokens)
      - Prompt Cached (90% discount): effective header overhead = 0.10 * header_tokens
    """
    saving_per_msg = baseline_avg - wire_avg
    if saving_per_msg <= 0:
        return {
            "saving_per_msg": round(saving_per_msg, 2),
            "uncached_breakeven_msgs": None,
            "cached_90pct_breakeven_msgs": None,
        }
    uncached_be = math.ceil(header_tokens / saving_per_msg)
    cached_be = math.ceil((header_tokens * 0.10) / saving_per_msg)
    return {
        "saving_per_msg": round(saving_per_msg, 2),
        "uncached_breakeven_msgs": max(1, uncached_be),
        "cached_90pct_breakeven_msgs": max(1, cached_be),
    }


def run_fair_benchmark(header_tokens: int = 1000) -> Dict[str, Any]:
    codec = ElegantCodec()
    scenarios = build_scenarios(codec)

    format_keys = [
        ("verbose_a2a", "1. Verbose A2A (Baseline)", "Yes (Prose+JSON)", "Yes"),
        ("structured_tool_json", "2. Structured Tool JSON", "Yes (Full JSON)", "Yes"),
        ("minified_key_json", "3. Minified Key JSON", "Yes (Short Keys)", "Yes"),
        ("simplified_template", "4. Simplified Template", "No (Lossy Flat)", "No"),
        ("toai_demotic_wire", "5. TOAI Demotic Wire", "Yes (Causal AST)", "Yes"),
    ]

    totals_o200k = {k: 0 for k, _, _, _ in format_keys}
    totals_cl100k = {k: 0 for k, _, _, _ in format_keys}
    totals_chars = {k: 0 for k, _, _, _ in format_keys}
    is_estimated = False
    encoding_label = ""

    per_scenario_results = []
    for sc in scenarios:
        sc_row = {"id": sc["id"], "title": sc["title"], "formats": {}}
        for k, label, _, _ in format_keys:
            m = measure_all_tokenizers(sc[k])
            is_estimated = m["is_estimated"]
            encoding_label = m["encoding_label"]
            totals_o200k[k] += m["o200k_tokens"]
            totals_cl100k[k] += m["cl100k_tokens"]
            totals_chars[k] += m["chars"]
            sc_row["formats"][k] = m
        per_scenario_results.append(sc_row)

    n = len(scenarios)
    avg_o200k = {k: totals_o200k[k] / n for k, _, _, _ in format_keys}
    avg_cl100k = {k: totals_cl100k[k] / n for k, _, _, _ in format_keys}
    avg_chars = {k: totals_chars[k] / n for k, _, _, _ in format_keys}

    wire_avg = avg_o200k["toai_demotic_wire"]

    # Measure token count of single Compact ID symbols (e.g. §S01, §X64, §G48)
    sample_symbols = ["§S01", "§G48", "§C20", "§X64", "§X354"]
    sym_token_counts = {s: count_bpe_tokens(s, "o200k_base")["tokens"] for s in sample_symbols}

    print("=" * 92)
    print("  ⚖️  TOAI-elegant-lang v5.4.3 Fair Multi-Format Benchmark & Amortization Analysis")
    print("=" * 92)
    print(f"  Tokenizer Backend : {encoding_label}")
    print(f"  Scenarios Tested  : {n} multi-agent coordination scenarios")
    print(f"  Tokens per §-ID   : {sym_token_counts} (2-3 BPE tokens: '§' + Prefix + Digits)")
    print("-" * 92)
    print(
        f"  {'Format Representation':<27} | {'Avg Chars':>9} | {'o200k Tok':>9} | {'cl100k Tok':>10} | {'vs Wire Diff':>12} | {'Causal Graph':<16}"
    )
    print("-" * 92)

    summary_rows = []
    for k, label, graph_support, _ in format_keys:
        o_tok = avg_o200k[k]
        c_tok = avg_cl100k[k]
        ch = avg_chars[k]
        if k == "toai_demotic_wire":
            diff_str = "BASELINE"
            rel_pct = 0.0
        else:
            rel_pct = (1.0 - (wire_avg / o_tok)) * 100.0 if o_tok > 0 else 0.0
            diff_str = f"{-rel_pct:+.1f}% saved" if rel_pct >= 0 else f"{-rel_pct:+.1f}% more"
        print(
            f"  {label:<27} | {ch:>9.1f} | {o_tok:>9.1f} | {c_tok:>10.1f} | {diff_str:>12} | {graph_support:<16}"
        )
        summary_rows.append({
            "key": k,
            "label": label,
            "avg_chars": round(ch, 1),
            "avg_o200k_tokens": round(o_tok, 1),
            "avg_cl100k_tokens": round(c_tok, 1),
            "wire_reduction_percent": round(rel_pct, 2),
            "preserves_causal_graph": graph_support,
        })

    print("-" * 92)
    print(f"\n  📉 Session Header Amortization / Break-Even Analysis (System Dictionary Header = {header_tokens} tokens)")
    print("  " + "-" * 88)
    print(
        f"  {'Comparison Target':<27} | {'Target Tok/Msg':>14} | {'Wire Tok/Msg':>12} | {'Saved/Msg':>10} | {'Break-Even (Std)':>16} | {'Break-Even (90% Cache)':>22}"
    )
    print("  " + "-" * 88)

    breakeven_table = {}
    for k, label in [
        ("verbose_a2a", "Verbose A2A (Baseline)"),
        ("structured_tool_json", "Structured Tool JSON"),
        ("minified_key_json", "Minified Key JSON"),
    ]:
        be = compute_breakeven_messages(header_tokens, avg_o200k[k], wire_avg)
        breakeven_table[k] = be
        std_str = f"{be['uncached_breakeven_msgs']} msgs" if be["uncached_breakeven_msgs"] else "N/A"
        cac_str = f"{be['cached_90pct_breakeven_msgs']} msgs" if be["cached_90pct_breakeven_msgs"] else "N/A"
        print(
            f"  {label:<27} | {avg_o200k[k]:>14.1f} | {wire_avg:>12.1f} | {be['saving_per_msg']:>10.1f} | {std_str:>16} | {cac_str:>22}"
        )
    print("=" * 92)

    return {
        "tokenizer_is_estimated": is_estimated,
        "encoding_label": encoding_label,
        "header_tokens_assumed": header_tokens,
        "symbol_token_counts": sym_token_counts,
        "summary": summary_rows,
        "breakeven": breakeven_table,
        "scenarios": per_scenario_results,
    }


if __name__ == "__main__":
    run_fair_benchmark()
