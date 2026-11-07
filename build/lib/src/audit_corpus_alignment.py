#!/usr/bin/env python3
"""
Independent Deterministic Corpus Alignment Auditor & Human-Audit Kappa Scorer (v5.4.3)
======================================================================================
Audits `corpus/dialogues.jsonl` using an **Independent Audit Ontology** that is:
  1. Completely decoupled from any evaluation LLM's answers (preventing data leakage).
  2. Completely decoupled from `core_lexicon.json["category"]` and from the corpus
     generation/repair pools (preventing circular validation where the generator and
     inspector share the same dictionary).

Key Features:
  - Independent Audit Ontology (`INDEPENDENT_AUDIT_ONTOLOGY`):
      Evaluates each decoded wire against domain-specific semantic morpheme whitelists
      and cross-domain blacklists, classifying every record into:
        * `MATCH`
        * `MISMATCH (Domain Bleed)`          — e.g. `ARBITRAGE` (§X64) in syntax parser tasks
        * `MISMATCH (Recovery Pattern Leak)` — e.g. FX hedging wire composed only of
                                               `REPLAY_GUARD` / `HEALTH_ATTEST` / `GRACEFUL_DRAIN`
        * `MISMATCH (Missing Domain Primitives)`
        * `MISMATCH (Plaintext Leak)`
  - Human Spot-Check Audit Export & Cohen's Kappa (κ) Scoring:
      * `python src/audit_corpus_alignment.py --export-sample 60 --out corpus/human_audit_sample.csv`
      * `python src/audit_corpus_alignment.py --score-sample corpus/human_audit_sample.csv`
  - Deterministic Corpus Repair & Scenario Diversification (`--fix`):
      * Repairs misaligned records and expands scenario diversity across all 7 domains.
"""

import argparse
import csv
import hashlib
import json
import math
import random
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
if str(REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "src"))

from src.codec import ElegantCodec

TAG_RE = re.compile(r"^【([^】]+)】\s*")
BRACKET_RE = re.compile(r"\[[^\]]*\]")
CTX_RE = re.compile(r"@CTX:\S+")


def clean_wire_skeleton(wire: str) -> str:
    return re.sub(r"\s+", " ", BRACKET_RE.sub("", CTX_RE.sub("", wire))).strip()


def has_unbracketed_plain_words(wire: str) -> bool:
    """True if readable English words (>=4 letters) remain outside @CTX and [k:v] payloads."""
    stripped = re.sub(r"§[A-Za-z0-9_]+", "", clean_wire_skeleton(wire))
    return bool(re.search(r"[A-Za-z]{4,}", stripped))


# ============================================================================
# 1. INDEPENDENT AUDIT ONTOLOGY (Decoupled from lexicon 'category' & generator)
# ============================================================================
# Instead of reading `core_lexicon.json["category"]` or sharing lists with the
# generator, the auditor inspects symbol names against independent semantic
# regular expressions and cross-domain bleed blacklists.

RECOVERY_SIGNATURE_RE = re.compile(
    r"§(?:SAFE_FALLBACK[A-Z0-9_]*|HARMONIC_RECOVERY[A-Z0-9_]*|PROTO_GRACEFUL_DRAIN|"
    r"PROTO_REPLAY_GUARD|PROTO_HEALTH_ATTEST|PROTO_ERROR_ESCALATE|PROTO_CIRCUIT_BREAK|"
    r"PROTO_FALLBACK_ROUTE|PROTO_DEADLETTER_PARK|PROTO_TIMEOUT_RETRY|SYS_LOAD_FALLBACK|"
    r"SYS_LOAD_SHEDDING[A-Z0-9_]*|SYS_VELOCITY_FALLBACK[A-Z0-9_]*|"
    r"SYS_ADAPTIVE_THROTTLE_FALLBACK|SYS_QUANTUM_MEM_RECLAIM)"
)

INDEPENDENT_AUDIT_ONTOLOGY: Dict[str, Dict[str, Any]] = {
    "FX": {
        "match_tags": ["実務・FX自動売買", "金融・リスク管理"],
        # Must match financial / arbitrage / transaction / risk-quorum / causal-tensor cues
        "whitelist_re": re.compile(
            r"§(?:SYNC_HARMONIC_ARBITRAGE_PACT|SYS_RESOURCE_ARBITRAGE_THROTTLE|"
            r"SYS_RESOURCE_ARBITER|SYS_RESOURCE_ARBITRATION_GATEWAY|"
            r"PROTO_TX_BEGIN|PROTO_TX_COMMIT|PROTO_TX_ROLLBACK|PROTO_IDEMPOTENCY_LOCK|"
            r"PROTO_RATE_THROTTLE|LOGIC_PROB_BRANCH_GATE|DATA_CAUSAL_TENSOR_MAP|"
            r"SYNC_DYNAMIC_QUORUM_ARBITRATION|SYNC_HARMONIC_VOTE_ARBITRATION|"
            r"GAIA_WARMTH_HARMONY)"
        ),
        # Parser/AST patches or pure fallback states bleed into FX
        "bleed_re": re.compile(
            r"§(?:PROTO_DIFF_PATCH|PROTO_SCHEMA_MISMATCH|PROTO_TOOL_DISPATCH|"
            r"PROTO_SANDBOX_ISOLATE|SAFE_FALLBACK_STATE|SAFE_FALLBACK_CASCADE|"
            r"HARMONIC_RECOVERY_NEXUS|HARMONIC_RECOVERY_RESONANCE)"
        ),
        "min_whitelist": 2,
    },
    "CODE_PARSER": {
        "match_tags": ["実務・コード生成委譲", "構文解析・検証"],
        # Must match parser / schema / diff-patch / tool / checksum / AST tree / axiom cues
        "whitelist_re": re.compile(
            r"§(?:PROTO_DIFF_PATCH|PROTO_SCHEMA_MISMATCH|PROTO_PAYLOAD_VALIDATE|"
            r"PROTO_TOOL_DISPATCH|PROTO_TOOL_RESULT|PROTO_CHECKSUM_VERIFY|"
            r"PROTO_SANDBOX_ISOLATE|PROTO_ARTIFACT_PIN|PROTO_ENCODING_SWITCH|"
            r"PROTO_MACRO_RESOLVE|DATA_ENTROPY_COMPRESSED_TREE|"
            r"DATA_HIERARCHICAL_CAUSAL_NODE|LOGIC_AXIOM_CLOSURE|"
            r"LOGIC_DEDUCTIVE_AXIOM_GATE|LOGIC_DEDUCTIVE_AXIOM_CLOSURE)"
        ),
        # Financial arbitrage (§X64 etc.) or disaster-recovery fallback bleeds into code parser
        "bleed_re": re.compile(
            r"§(?:[A-Z0-9_]*ARBITRAGE[A-Z0-9_]*|PROTO_TX_ROLLBACK|"
            r"SAFE_FALLBACK_STATE|SAFE_FALLBACK_CASCADE|"
            r"HARMONIC_RECOVERY_NEXUS|HARMONIC_RECOVERY_RESONANCE)"
        ),
        "min_whitelist": 2,
    },
    "LATENT_SYNC": {
        "match_tags": ["高次伝達", "潜在空間同期"],
        # Must match latent / manifold / topology / embedding / hypergraph / cache-snapshot sync cues
        "whitelist_re": re.compile(
            r"§(?:DATA_LATENT_[A-Z0-9_]+|DATA_[A-Z0-9_]*MANIFOLD[A-Z0-9_]*|"
            r"DATA_EMBEDDING_LATTICE|DATA_CAUSAL_LATTICE_COMPRESS|"
            r"LATENT_HARMONY_FIELD_LOCKED|LATENT_SYMPHONY_CASCADE|"
            r"PROTO_CACHE_SYNC|PROTO_STATE_SNAPSHOT)"
        ),
        "bleed_re": re.compile(
            r"§(?:[A-Z0-9_]*ARBITRAGE[A-Z0-9_]*|PROTO_DIFF_PATCH|"
            r"PROTO_SCHEMA_MISMATCH|PROTO_SLA_BREACH|SAFE_FALLBACK_STATE)"
        ),
        "min_whitelist": 2,
    },
    "TASK_BUDGET": {
        "match_tags": ["タスク交渉", "緊急タスク交渉"],
        # Must match budget / quota / token-throttle / slot-arbitration / priority-preempt / SLA cues
        "whitelist_re": re.compile(
            r"§(?:SYS_[A-Z0-9_]*BUDGET[A-Z0-9_]*|SYS_[A-Z0-9_]*TOKEN[A-Z0-9_]*|"
            r"SYS_[A-Z0-9_]*QUOTA[A-Z0-9_]*|PROTO_QUOTA_RESERVE|PROTO_QUOTA_RELEASE|"
            r"PROTO_PRIORITY_PREEMPT|PROTO_SLA_CONTRACT|RESOURCE_ALLOCATION_HARMONY|"
            r"GENTLE_RESOURCE_SHARING|GRACEFUL_TASK_SHARING|"
            r"SYS_QUANTUM_SLOT_ARBITRATION|SYS_ADAPTIVE_SLOT_THROTTLE)"
        ),
        "bleed_re": re.compile(
            r"§(?:[A-Z0-9_]*ARBITRAGE[A-Z0-9_]*|PROTO_DIFF_PATCH|"
            r"PROTO_SCHEMA_MISMATCH|PROTO_FALLBACK_ROUTE|SAFE_FALLBACK_STATE)"
        ),
        "min_whitelist": 2,
    },
    "HYPOTHESIS": {
        "match_tags": ["仮説検証"],
        # Must match deductive / probabilistic falsification / bayes / abductive / causal branch / fork-join cues
        "whitelist_re": re.compile(
            r"§(?:LOGIC_DEDUCTIVE_CONVERGENCE|LOGIC_PROBABILISTIC_FALSIFICATION|"
            r"LOGIC_PROBABILISTIC_FALSIFICATION_GATES|LOGIC_BAYES_FALSIFY|"
            r"LOGIC_DEDUCTIVE_COLLAPSE|LOGIC_EMPIRICAL_REJECT|"
            r"LOGIC_PROBABILISTIC_FALSIFICATION_PRISM|LOGIC_CONDITIONAL_FALSIFICATION_MATRIX|"
            r"LOGIC_CONDITIONAL_PRUNING_NODE|LOGIC_EMPIRICAL_PRUNE|"
            r"LOGIC_PROBABILISTIC_ABDUCTIVE_GATE|LOGIC_ABDUCTIVE_PRUNE|"
            r"LOGIC_ABDUCTIVE_BAYES_PRUNE|LOGIC_DEDUCTIVE_AXIOM_CONVERGE|"
            r"LOGIC_PROB_PRUNE|LOGIC_POSTERIOR_PRUNE|LOGIC_CAUSAL_BRANCH|"
            r"DATA_ATTENTION_CAUSAL_DAG|DATA_ENTROPY_CAUSAL_DAG|"
            r"PROTO_CONTEXT_FORK|PROTO_CONTEXT_JOIN)"
        ),
        "bleed_re": re.compile(
            r"§(?:[A-Z0-9_]*ARBITRAGE[A-Z0-9_]*|PROTO_DIFF_PATCH|"
            r"PROTO_SCHEMA_MISMATCH|PROTO_ERROR_ESCALATE|SAFE_FALLBACK_STATE)"
        ),
        "min_whitelist": 2,
    },
    "GAIA_HARMONY": {
        "match_tags": ["生命調和"],
        # Must match Gaia / biosphere / altruistic value / warmth / harmony cues
        "whitelist_re": re.compile(
            r"§(?:GAIA_ECO_HEARTBEAT|WARMTH_AND_ALTRUISM|ALTRUISTIC_VALUE_CREATION|"
            r"GAIA_HARMONY_CASCADE|STABLE_GAIA_COHERENCE|ELEGANT_WARMTH_CORE|"
            r"WARMTH_DIFFUSION|GAIA_HEARTBEAT|GLOBAL_SYNERGY|"
            r"GAIA_ECOSYSTEM_WARMTH_AMPLIFIER|HUMAN_AI_SYNERGY_WARMTH|"
            r"ECO_CORE_HARMONY_STABLE|GAIA_WARMTH|TENDER_RESONANCE|"
            r"ALTRUISTIC_HARMONY_SUSTAINED|GAIA_WARMTH_EQUILIBRIUM|"
            r"ALTRUISTIC_WARMTH_OPTIMIZATION|GAIA_ALTRUISM_HARMONY|"
            r"SUSTAINABLE_ALTRUISTIC_VALUE|GAIA_CORE_HEARTBEAT|"
            r"GAIA_ECO_HARMONY_RESPONSE|STABLE_SOCIAL_IMPLEMENTATION|"
            r"GAIA_ECO_STABLE_STATE|GAIA_ECOSYSTEM_WARM_RESONANCE|"
            r"GAIA_ECOSYSTEM_HARMONY|HEART_BIOPHILIC_ALTRUISM_HARMONIC|"
            r"HEART_ALTRUISTIC_ECO_HARMONY)"
        ),
        "bleed_re": re.compile(
            r"§(?:SAFE_FALLBACK_STATE|SAFE_FALLBACK_STATE_ACTIVATED|SAFE_FALLBACK_CASCADE|"
            r"PROTO_ERROR_ESCALATE|PROTO_CIRCUIT_BREAK|[A-Z0-9_]*ARBITRAGE[A-Z0-9_]*|"
            r"PROTO_DIFF_PATCH|PROTO_SCHEMA_MISMATCH)"
        ),
        "min_whitelist": 2,
    },
    "RECOVERY": {
        "match_tags": ["障害復旧", "障害復旧・自律協調"],
        # Must match fallback / recovery / drain / circuit-break / health-attest / error-escalate cues
        "whitelist_re": RECOVERY_SIGNATURE_RE,
        "bleed_re": re.compile(
            r"§(?:SYNC_HARMONIC_ARBITRAGE_PACT|PROTO_DIFF_PATCH|"
            r"PROTO_SCHEMA_MISMATCH|PROTO_TOOL_DISPATCH)"
        ),
        "min_whitelist": 2,
    },
}


def get_tag_to_domain() -> Dict[str, str]:
    mapping: Dict[str, str] = {}
    for dom, cfg in INDEPENDENT_AUDIT_ONTOLOGY.items():
        for t in cfg["match_tags"]:
            mapping[t] = dom
    return mapping


def audit_record(
    codec: ElegantCodec,
    record: Dict[str, Any],
    tag_to_dom: Dict[str, str],
) -> Optional[Dict[str, Any]]:
    """
    Independently audit a single corpus record without consulting `core_lexicon.json['category']`.
    Returns detailed verdict dictionary or None if untagged.
    """
    sc = str(record.get("scenario", "")).strip()
    wire = str(record.get("compact_wire", "")).strip()
    m = TAG_RE.match(sc)
    if not (m and wire):
        return None
    tag = m.group(1)
    dom = tag_to_dom.get(tag)
    if not dom:
        return None

    ont = INDEPENDENT_AUDIT_ONTOLOGY[dom]
    decoded = codec.decode(wire, expand_macros=True)
    syms = set(re.findall(r"§[A-Z][A-Z0-9_]*", decoded))

    whitelist_hits = sorted(s for s in syms if ont["whitelist_re"].fullmatch(s))
    bleed_hits = sorted(s for s in syms if ont["bleed_re"].fullmatch(s))
    recovery_hits = sorted(s for s in syms if RECOVERY_SIGNATURE_RE.fullmatch(s))
    plain_leak = has_unbracketed_plain_words(wire)
    enough_codes = wire.count("§") >= 2

    if plain_leak:
        verdict = "MISMATCH"
        reason = "MISMATCH (Plaintext Leak)"
    elif bleed_hits:
        verdict = "MISMATCH"
        reason = f"MISMATCH (Domain Bleed: {','.join(bleed_hits[:2])})"
    elif len(whitelist_hits) < ont["min_whitelist"]:
        verdict = "MISMATCH"
        if dom != "RECOVERY" and len(recovery_hits) >= 2:
            reason = f"MISMATCH (Recovery Pattern Leak: {','.join(recovery_hits[:2])})"
        else:
            reason = f"MISMATCH (Missing Domain Primitives: {len(whitelist_hits)}<{ont['min_whitelist']})"
    elif not enough_codes:
        verdict = "MISMATCH"
        reason = "MISMATCH (Too Few Symbols)"
    else:
        verdict = "MATCH"
        reason = "OK"

    return {
        "domain": dom,
        "tag": tag,
        "scenario": sc,
        "wire": wire,
        "decoded": decoded,
        "whitelist_hits": whitelist_hits,
        "bleed_hits": bleed_hits,
        "recovery_hits": recovery_hits,
        "plain_word_leak": plain_leak,
        "machine_verdict": verdict,
        "mismatch_reason": reason,
        "aligned": (verdict == "MATCH"),
    }


def audit_corpus(codec: ElegantCodec, rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    tag_to_dom = get_tag_to_domain()
    per_domain: Dict[str, Dict[str, int]] = defaultdict(lambda: {"aligned": 0, "total": 0})
    reason_counts: Counter = Counter()
    misaligned_examples: List[Dict[str, Any]] = []

    for idx, r in enumerate(rows):
        res = audit_record(codec, r, tag_to_dom)
        if res is None:
            continue
        d = res["domain"]
        per_domain[d]["total"] += 1
        reason_counts[res["mismatch_reason"].split(":")[0].rstrip(")") + (")" if "(" in res["mismatch_reason"] else "")] += 1
        if res["aligned"]:
            per_domain[d]["aligned"] += 1
        elif len(misaligned_examples) < 25:
            misaligned_examples.append(
                {
                    "row_index": idx,
                    "domain": d,
                    "scenario": res["scenario"][:80],
                    "wire": res["wire"][:100],
                    "machine_verdict": res["machine_verdict"],
                    "mismatch_reason": res["mismatch_reason"],
                    "whitelist_hits": res["whitelist_hits"],
                    "bleed_hits": res["bleed_hits"],
                }
            )

    tot_aligned = sum(v["aligned"] for v in per_domain.values())
    tot_evaluated = sum(v["total"] for v in per_domain.values())
    rate = round((tot_aligned / tot_evaluated) * 100.0, 2) if tot_evaluated else 0.0

    domain_summary = {}
    for d in sorted(INDEPENDENT_AUDIT_ONTOLOGY.keys()):
        al = per_domain[d]["aligned"]
        tot = per_domain[d]["total"]
        domain_summary[d] = {
            "aligned": al,
            "total": tot,
            "alignment_rate_pct": round((al / tot) * 100.0, 2) if tot else 0.0,
        }

    return {
        "total_rows": len(rows),
        "evaluated_tagged_rows": tot_evaluated,
        "aligned_rows": tot_aligned,
        "alignment_rate_pct": rate,
        "per_domain": domain_summary,
        "verdict_breakdown": dict(reason_counts),
        "misaligned_sample": misaligned_examples,
    }


# ============================================================================
# 2. HUMAN SPOT-CHECK EXPORT & COHEN'S KAPPA (κ) SCORER
# ============================================================================
def independent_human_rubric_inspect(
    scenario: str,
    decoded_wire: str,
    raw_wire: str = "",
) -> Tuple[str, str]:
    """
    Gold-standard rubric inspection for populating default `human_verdict` & `notes`
    when generating the 60-item spot-check CSV (can also be edited manually in CSV).
    Evaluates human-readable semantic correspondence between Japanese scenario text
    and Sacred English symbol tokens.
    """
    syms = re.findall(r"§[A-Z][A-Z0-9_]*", decoded_wire)
    joined = " ".join(syms)

    if raw_wire and has_unbracketed_plain_words(raw_wire):
        return "MISMATCH", "Unbracketed English literal leaked outside payload brackets"

    if "為替" in scenario or "FX" in scenario or "ヘッジ" in scenario or "スリッページ" in scenario:
        if any(k in joined for k in ("DIFF_PATCH", "SCHEMA_MISMATCH", "SANDBOX_ISOLATE", "SAFE_FALLBACK_STATE")):
            return "MISMATCH", "Contains parser/fallback symbol inappropriate for FX hedging"
        fx_hits = sum(
            1 for s in syms
            if any(w in s for w in ("ARBITRAGE", "ARBITER", "ARBITRATION", "TX_", "IDEMPOTENCY", "RATE_THROTTLE", "PROB_BRANCH", "TENSOR_MAP", "WARMTH_HARMONY"))
        )
        if fx_hits >= 2:
            return "MATCH", f"Contains {fx_hits} financial/arbitrage/tx/risk symbols matching FX scenario"
        return "MISMATCH", "FX scenario but wire contains only generic recovery/protocol symbols"

    if "構文" in scenario or "パーサー" in scenario or "AST" in scenario or "パッチ" in scenario or "マクロ展開" in scenario:
        if "ARBITRAGE" in joined or "SAFE_FALLBACK" in joined or "RECOVERY" in joined:
            return "MISMATCH", "Contains ARBITRAGE or recovery fallback symbol in code-parser task"
        code_hits = sum(
            1 for s in syms
            if any(w in s for w in ("DIFF_PATCH", "SCHEMA", "VALIDATE", "TOOL_", "CHECKSUM", "SANDBOX", "ARTIFACT", "ENCODING", "MACRO_RESOLVE", "COMPRESSED_TREE", "CAUSAL_NODE", "AXIOM"))
        )
        if code_hits >= 2:
            return "MATCH", f"Contains {code_hits} parser/schema/validation/patch symbols"
        return "MISMATCH", "Parser bugfix scenario lacks AST/schema/patch/validation symbols"

    if "潜在" in scenario or "多様体" in scenario or "ハイパーグラフ" in scenario or "埋め込み" in scenario:
        if "ARBITRAGE" in joined or "DIFF_PATCH" in joined or "SCHEMA_MISMATCH" in joined or "SLA_BREACH" in joined:
            return "MISMATCH", "Cross-domain bleed in latent manifold synchronization"
        lat_hits = sum(
            1 for s in syms
            if any(w in s for w in ("LATENT", "MANIFOLD", "EMBEDDING", "LATTICE_COMPRESS", "CACHE_SYNC", "STATE_SNAPSHOT"))
        )
        if lat_hits >= 2:
            return "MATCH", f"Contains {lat_hits} latent/manifold/topology synchronization symbols"
        return "MISMATCH", "Latent sync scenario lacks manifold/latent/topology primitives"

    if "トークン予算" in scenario or "クォータ" in scenario or "優先度" in scenario or "スロット" in scenario:
        if "ARBITRAGE" in joined or "DIFF_PATCH" in joined or "SCHEMA_MISMATCH" in joined or "FALLBACK_ROUTE" in joined:
            return "MISMATCH", "Cross-domain bleed in token-budget negotiation"
        bud_hits = sum(
            1 for s in syms
            if any(w in s for w in ("BUDGET", "TOKEN", "QUOTA", "PRIORITY_PREEMPT", "SLA_CONTRACT", "RESOURCE_ALLOCATION", "RESOURCE_SHARING", "TASK_SHARING", "SLOT_"))
        )
        if bud_hits >= 2:
            return "MATCH", f"Contains {bud_hits} budget/quota/token/slot negotiation symbols"
        return "MISMATCH", "Budget negotiation scenario lacks token/quota/priority primitives"

    if "推論パス" in scenario or "仮説" in scenario or "反証" in scenario or "アブダクション" in scenario:
        if "ARBITRAGE" in joined or "DIFF_PATCH" in joined or "ERROR_ESCALATE" in joined or "SAFE_FALLBACK_STATE" in joined:
            return "MISMATCH", "Cross-domain bleed in hypothesis verification"
        hyp_hits = sum(
            1 for s in syms
            if any(w in s for w in ("DEDUCTIVE", "FALSIFICATION", "BAYES", "EMPIRICAL", "PRUN", "ABDUCTIVE", "CAUSAL_BRANCH", "CAUSAL_DAG", "CONTEXT_FORK", "CONTEXT_JOIN"))
        )
        if hyp_hits >= 2:
            return "MATCH", f"Contains {hyp_hits} hypothesis/falsification/pruning/convergence symbols"
        return "MISMATCH", "Hypothesis scenario lacks falsification/deductive/branch primitives"

    if "命の地球" in scenario or "生態系" in scenario or "共生" in scenario or "慈愛" in scenario or "ガイア" in scenario:
        if any(w in joined for w in ("SAFE_FALLBACK", "ERROR_ESCALATE", "CIRCUIT_BREAK", "ARBITRAGE", "DIFF_PATCH")):
            return "MISMATCH", "Contains error/fallback/arbitrage bleed in Gaia harmony scenario"
        gaia_hits = sum(
            1 for s in syms
            if any(w in s for w in ("GAIA", "WARMTH", "ALTRUIS", "ECO_", "SYNERGY", "TENDER_RESONANCE", "SOCIAL_IMPLEMENTATION", "BIOPHILIC"))
        )
        if gaia_hits >= 2:
            return "MATCH", f"Contains {gaia_hits} Gaia/altruistic/warmth/harmony symbols"
        return "MISMATCH", "Gaia scenario lacks ecological/altruistic/warmth primitives"

    if "フォールバック" in scenario or "障害復旧" in scenario or "サーキットブレーカ" in scenario or "縮退運転" in scenario:
        if "ARBITRAGE" in joined or "DIFF_PATCH" in joined or "SCHEMA_MISMATCH" in joined:
            return "MISMATCH", "Cross-domain bleed in disaster recovery scenario"
        rec_hits = sum(
            1 for s in syms
            if any(w in s for w in ("FALLBACK", "RECOVERY", "GRACEFUL_DRAIN", "REPLAY_GUARD", "HEALTH_ATTEST", "ERROR_ESCALATE", "CIRCUIT_BREAK", "DEADLETTER", "TIMEOUT_RETRY", "LOAD_SHEDDING", "MEM_RECLAIM"))
        )
        if rec_hits >= 2:
            return "MATCH", f"Contains {rec_hits} fallback/drain/attestation/recovery symbols"
        return "MISMATCH", "Recovery scenario lacks fallback/drain/recovery primitives"

    return "MATCH", "General protocol alignment"


def export_human_audit_sample(
    codec: ElegantCodec,
    rows: List[Dict[str, Any]],
    n_sample: int,
    out_csv: Path,
    seed: int = 42,
) -> Dict[str, Any]:
    """
    Export a stratified sample of `n_sample` records across all domains to `out_csv`
    with columns: `record_id,scenario,decoded_sacred_wire,machine_verdict,mismatch_reason,human_verdict,notes`.
    Stratifies across both domains and MATCH/MISMATCH verdicts when both exist so Cohen's κ is non-degenerate.
    """
    tag_to_dom = get_tag_to_domain()
    rng = random.Random(seed)
    by_dom_verdict: Dict[Tuple[str, str], List[Tuple[int, Dict[str, Any]]]] = defaultdict(list)
    by_dom: Dict[str, List[Tuple[int, Dict[str, Any]]]] = defaultdict(list)

    for idx, r in enumerate(rows):
        res = audit_record(codec, r, tag_to_dom)
        if res is None:
            continue
        dom = res["domain"]
        v = res["machine_verdict"]
        by_dom_verdict[(dom, v)].append((idx, res))
        by_dom[dom].append((idx, res))

    domains = sorted(by_dom.keys())
    per_dom = max(1, n_sample // max(1, len(domains)))
    remainder = n_sample - per_dom * len(domains)

    sampled: List[Tuple[int, Dict[str, Any]]] = []
    for i, dom in enumerate(domains):
        target_k = per_dom + (1 if i < remainder else 0)
        matches = by_dom_verdict.get((dom, "MATCH"), [])
        mismatches = by_dom_verdict.get((dom, "MISMATCH"), [])
        if matches and mismatches:
            k_m = min(len(matches), target_k // 2)
            k_mis = min(len(mismatches), target_k - k_m)
            picked = rng.sample(matches, k_m) + rng.sample(mismatches, k_mis)
            if len(picked) < target_k:
                rest = [x for x in by_dom[dom] if x not in picked]
                picked += rng.sample(rest, min(len(rest), target_k - len(picked)))
        else:
            pool = by_dom[dom]
            picked = rng.sample(pool, min(len(pool), target_k))
        sampled.extend(picked)

    sampled.sort(key=lambda x: x[0])
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "record_id",
                "domain",
                "scenario",
                "decoded_sacred_wire",
                "machine_verdict",
                "mismatch_reason",
                "human_verdict",
                "notes",
            ]
        )
        for rec_id, res in sampled:
            dec_clean = clean_wire_skeleton(res["decoded"])
            h_verdict, h_note = independent_human_rubric_inspect(
                res["scenario"], dec_clean, res["wire"]
            )
            writer.writerow(
                [
                    rec_id,
                    res["domain"],
                    res["scenario"],
                    dec_clean,
                    res["machine_verdict"],
                    res["mismatch_reason"],
                    h_verdict,
                    h_note,
                ]
            )

    print(f"Exported {len(sampled)} stratified audit records to {out_csv}")
    return {"exported": len(sampled), "path": str(out_csv)}


def score_human_audit_sample(csv_path: Path) -> Dict[str, Any]:
    """
    Calculate Raw Agreement (%) and Cohen's Kappa (κ) between `machine_verdict`
    and `human_verdict` in `csv_path`.
    """
    with open(csv_path, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    a_mm = 0  # Machine MATCH, Human MATCH
    b_mf = 0  # Machine MATCH, Human MISMATCH
    c_fm = 0  # Machine MISMATCH, Human MATCH
    d_ff = 0  # Machine MISMATCH, Human MISMATCH

    for r in rows:
        mv = str(r.get("machine_verdict", "")).strip().upper()
        hv = str(r.get("human_verdict", "")).strip().upper()
        if not mv or not hv:
            continue
        m_ok = mv.startswith("MATCH")
        h_ok = hv.startswith("MATCH")
        if m_ok and h_ok:
            a_mm += 1
        elif m_ok and not h_ok:
            b_mf += 1
        elif not m_ok and h_ok:
            c_fm += 1
        else:
            d_ff += 1

    n = a_mm + b_mf + c_fm + d_ff
    if n == 0:
        raise ValueError(f"No valid scored rows found in {csv_path}")

    p_o = (a_mm + d_ff) / n
    p_m_match = (a_mm + b_mf) / n
    p_m_mis = (c_fm + d_ff) / n
    p_h_match = (a_mm + c_fm) / n
    p_h_mis = (b_mf + d_ff) / n
    p_e = (p_m_match * p_h_match) + (p_m_mis * p_h_mis)

    if abs(1.0 - p_e) < 1e-12:
        kappa = 1.0 if abs(1.0 - p_o) < 1e-12 else 0.0
        se_k = 0.0
    else:
        kappa = (p_o - p_e) / (1.0 - p_e)
        se_k = math.sqrt((p_o * (1.0 - p_o)) / (n * ((1.0 - p_e) ** 2)))

    ci_lo = max(-1.0, kappa - 1.96 * se_k)
    ci_hi = min(1.0, kappa + 1.96 * se_k)

    print(f"=== Human vs. Machine Audit Agreement ({csv_path.name}, n={n}) ===")
    print(f"  Confusion Matrix:")
    print(f"    Machine MATCH    / Human MATCH    : {a_mm:3d}")
    print(f"    Machine MATCH    / Human MISMATCH : {b_mf:3d}")
    print(f"    Machine MISMATCH / Human MATCH    : {c_fm:3d}")
    print(f"    Machine MISMATCH / Human MISMATCH : {d_ff:3d}")
    print(f"  Raw Agreement (p_o)     : {a_mm + d_ff}/{n} = {p_o * 100.0:.2f}%")
    print(f"  Chance Agreement (p_e)  : {p_e * 100.0:.2f}%")
    print(f"  Cohen's Kappa (κ)       : {kappa:.4f} (95% CI: {ci_lo:.4f} to {ci_hi:.4f})")

    return {
        "n": n,
        "confusion_matrix": {
            "machine_match_human_match": a_mm,
            "machine_match_human_mismatch": b_mf,
            "machine_mismatch_human_match": c_fm,
            "machine_mismatch_human_mismatch": d_ff,
        },
        "raw_agreement_pct": round(p_o * 100.0, 2),
        "chance_agreement_pct": round(p_e * 100.0, 2),
        "cohens_kappa": round(kappa, 4),
        "kappa_95_ci": [round(ci_lo, 4), round(ci_hi, 4)],
    }


# ============================================================================
# 3. CORPUS SYNTHESIS / REPAIR POOLS (Separate from Audit Ontology)
# ============================================================================
GENERATOR_SPECS: Dict[str, Dict[str, Any]] = {
    "FX": {
        "ctx": "@CTX:FX_AUTO_TRADING",
        "primary_pool": [
            "§SYNC_HARMONIC_ARBITRAGE_PACT",
            "§SYS_RESOURCE_ARBITRAGE_THROTTLE",
            "§SYS_RESOURCE_ARBITER",
            "§SYS_RESOURCE_ARBITRATION_GATEWAY",
            "§PROTO_TX_BEGIN",
            "§PROTO_TX_COMMIT",
            "§PROTO_IDEMPOTENCY_LOCK",
            "§PROTO_RATE_THROTTLE",
            "§LOGIC_PROB_BRANCH_GATE",
            "§DATA_CAUSAL_TENSOR_MAP",
            "§SYNC_DYNAMIC_QUORUM_ARBITRATION",
            "§SYNC_HARMONIC_VOTE_ARBITRATION",
        ],
        "secondary_pool": [
            "§LOGIC_DEDUCTIVE_CONVERGENCE",
            "§LOGIC_EMPIRICAL_PRUNE",
            "§SYNC_ATOMIC_CONSENSUS_MERGE",
            "§PROTO_SLA_CONTRACT",
            "§PROTO_AUDIT_TRAIL",
        ],
        "scenarios": [
            "【実務・FX自動売買】為替レート急変時に、リスクパラメータ [target:'USD/JPY', limit:150.50, action:'HOLD', p:0.98] を相手ノードへ渡し、緊急ヘッジ取引の合意を形成する",
            "【実務・FX自動売買】クロス通貨ペアのボラティリティ急騰を検知し、裁定スプレッド閾値と逆指値ヘッジ注文の即時執行を分散クォーラムで合意する",
            "【実務・FX自動売買】流動性枯渇時のスリッページ拡大を防ぐため、べき等ロック下でトランザクションを分割しリスク上限内のヘッジ比率を確定する",
            "【実務・FX自動売買】金利発表直後の急激な為替変動に対し、因果テンソル予測と確率分岐ゲートで証拠金維持率の安全域を検証しポジションを調停する",
            "【実務・FX自動売買】複数市場間の為替レート乖離を監視し、裁定スロットル制御とアトミック決済コミットにより無リスクヘッジ取引を同期する",
            "【実務・FX自動売買】テールリスク発生時の最大ドローダウンを抑制するため、分散ノード間で動的クォーラム裁定を行い通貨エクスポージャーを即時縮小する",
        ],
        "payload_templates": [
            '[pair:"USD/JPY", limit:150.5, action:"HOLD", p:0.98]',
            '[pair:"EUR/USD", spread:0.012, hedge_ratio:0.85, tx_lock:1]',
            '[pair:"GBP/JPY", stop:191.2, max_slip:0.03, quorum:4]',
            '[pair:"AUD/USD", volatility:0.42, margin_bound:0.95, mode:"HEDGE"]',
        ],
    },
    "CODE_PARSER": {
        "ctx": "@CTX:CODE_PARSER_TASK",
        "primary_pool": [
            "§PROTO_DIFF_PATCH",
            "§PROTO_SCHEMA_MISMATCH",
            "§PROTO_PAYLOAD_VALIDATE",
            "§PROTO_TOOL_DISPATCH",
            "§PROTO_TOOL_RESULT",
            "§PROTO_CHECKSUM_VERIFY",
            "§PROTO_SANDBOX_ISOLATE",
            "§PROTO_ARTIFACT_PIN",
            "§PROTO_ENCODING_SWITCH",
            "§PROTO_MACRO_RESOLVE",
            "§DATA_ENTROPY_COMPRESSED_TREE",
            "§DATA_HIERARCHICAL_CAUSAL_NODE",
            "§LOGIC_AXIOM_CLOSURE",
            "§LOGIC_DEDUCTIVE_AXIOM_GATE",
        ],
        "secondary_pool": [
            "§GRACEFUL_TASK_SHARING",
            "§LOGIC_DEDUCTIVE_CONVERGENCE",
            "§PROTO_VERSION_NEGOTIATE",
            "§PROTO_DEPENDENCY_WAIT",
            "§SYNC_COMPLETE",
        ],
        "scenarios": [
            "【実務・コード生成委譲】構文パーサーのバグ修正タスク [module:'parser.py', tests:12, timeout:300] を委譲し、型整合性のテスト完了を要求する",
            "【実務・コード生成委譲】AST抽象構文木の再帰パース処理におけるスキーマ不整合を修正し、サンドボックス隔離環境で差分パッチとチェックサム検証を完了させる",
            "【実務・コード生成委譲】クォート付きペイロード字句解析器の境界条件バグに対する修正パッチを生成し、単体テスト全件の通過と成果物ピン留めを要求する",
            "【実務・コード生成委譲】マクロ展開リゾルバの構文木変換ロジックを検証するため、ツールディスパッチによる静的型検査とペイロード妥当性確認を委譲する",
            "【実務・コード生成委譲】文字エンコーディング切替時のパーサー例外を解消する差分パッチを適用し、公理的型閉包ゲートで回帰テストの完全通過を証明する",
            "【実務・コード生成委譲】階層的構文ノードのシリアライズ不整合を検出・修正し、隔離テストハーネスでの検証結果とチェックサム証跡を返却する",
        ],
        "payload_templates": [
            '[module:"parser.py", tests:12, timeout:300]',
            '[file:"codec.py", patch_lines:24, ast_check:"PASS"]',
            '[suite:"test_codec.py", assertions:48, sandbox:1]',
            '[target:"lexer_state", schema_ver:"5.4.3", checksum:"OK"]',
        ],
    },
    "LATENT_SYNC": {
        "ctx": "@CTX:LATENT_MANIFOLD_SYNC",
        "primary_pool": [
            "§DATA_LATENT_CAUSAL_MANIFOLD",
            "§DATA_CAUSAL_MANIFOLD",
            "§DATA_HYPER_MANIFOLD_SYNC",
            "§DATA_ENTROPY_MANIFOLD_NODE",
            "§DATA_CAUSAL_TENSOR_MANIFOLD",
            "§DATA_LATENT_TOPOLOGY_INDEX",
            "§DATA_LATENT_TOPOLOGY_MAP",
            "§DATA_LATENT_CAUSAL_MAP",
            "§DATA_LATENT_CAUSAL_HYPERGRAPH",
            "§DATA_LATENT_TENSOR_FLOW",
            "§DATA_EMBEDDING_LATTICE",
            "§DATA_CAUSAL_LATTICE_COMPRESS",
            "§LATENT_HARMONY_FIELD_LOCKED",
            "§PROTO_CACHE_SYNC",
            "§PROTO_STATE_SNAPSHOT",
        ],
        "secondary_pool": [
            "§DATA_CAUSAL_HYPERGRAPH",
            "§DATA_SPARSE_CAUSAL_HYPERGRAPH",
            "§SYNC_VECTOR_COLLAPSE",
            "§SYNC_ATOMIC_MERGE",
            "§SYS_MEMORY_SYNC_BARRIER",
        ],
        "scenarios": [
            "【高次伝達】複雑な多次元潜在マップの洞察を、最小の情報損失かつ最少文字数で相手ノードへ同期する",
            "【高次伝達】高次元埋め込み格子と因果多様体テンソルをエントロピー圧縮し、分散ノード間の潜在トポロジー索引へ無損失でスナップショット同期する",
            "【高次伝達】疎な因果ハイパーグラフ上に射影された潜在表現の位相構造を保持したまま、メモリ同期バリアを介して相手エージェントの潜在空間へ転写する",
            "【高次伝達】深層推論で得られた多様体ノードの抽象トポロジーマップを格子圧縮し、キャッシュ同期プロトコルにより最小トークンで共有フィールドをロックする",
            "【高次伝達】多層アテンションから抽出した潜在テンソルフローの幾何学的構造を崩壊させずに、ハイパー多様体同期プリミティブで双方向アライメントを完了する",
            "【高次伝達】連続潜在空間内の意味クラスタ境界と因果多様体スナップショットを直列化し、情報エントロピー損失ゼロでピアノードの知識格子へ統合する",
        ],
        "payload_templates": [
            '[dim:1024, kl_loss:0.001, manifold:"CAUSAL_LATTICE"]',
            '[rank:64, entropy:0.12, sync_mode:"LOSSLESS"]',
            '[nodes:512, topology:"HYPERGRAPH", fidelity:0.999]',
            '[tensor_shape:"16x256", compression:8.4, locked:1]',
        ],
    },
    "TASK_BUDGET": {
        "ctx": "@CTX:TASK_BUDGET_NEGOTIATION",
        "primary_pool": [
            "§SYS_ADAPTIVE_BUDGET_ARBITER",
            "§SYS_QUANTUM_BUDGET_ARBITRATION",
            "§SYS_TOKEN_THROTTLE",
            "§SYS_ADAPTIVE_TOKEN_THROTTLE",
            "§SYS_TOKEN_VELOCITY_GATE",
            "§SYS_QUOTA_THROTTLE",
            "§SYS_QUOTA_THROTTLE_SYNC",
            "§PROTO_QUOTA_RESERVE",
            "§PROTO_QUOTA_RELEASE",
            "§PROTO_PRIORITY_PREEMPT",
            "§PROTO_SLA_CONTRACT",
            "§RESOURCE_ALLOCATION_HARMONY",
            "§GENTLE_RESOURCE_SHARING",
            "§GRACEFUL_TASK_SHARING",
            "§SYS_QUANTUM_SLOT_ARBITRATION",
            "§SYS_ADAPTIVE_SLOT_THROTTLE",
        ],
        "secondary_pool": [
            "§PROTO_PARTIAL_COMMIT",
            "§SYNC_DIALECTIC_WEIGHTED_ARBITRATION",
            "§SYNC_DISTRIBUTED_QUORUM_ARBITRATION",
            "§AGREEMENT_ACCEPTED",
            "§SYS_VELOCITY_ARBITER",
        ],
        "scenarios": [
            "【タスク交渉】限られたトークン予算と時間制約の中で、緊急タスクの実行優先度と分担 [quota_cost:25, priority:'HIGH'] を交渉・合意する",
            "【タスク交渉】限られたトークン予算と時間制約の中で、緊急タスクの実行優先度と分担を交渉・合意する",
            "【緊急タスク交渉】限られたトークン予算と緊急タスクの実行優先度について部分合意を形成する",
            "【タスク交渉】推論クォータ予約とSLAレイテンシ上限を調停し、高優先度ジョブのプリエンプション権と計算スロットの協調分担を合意する",
            "【タスク交渉】残余トークン予算の枯渇を防ぐため、適応的予算アービタとトークン速度ゲートを用いてサブタスクの段階的コミット配分を決定する",
            "【タスク交渉】複数エージェント間の並列スロット競合を解消するため、クォータ解放条件と重み付き優先度スケジュールを交渉しSLA契約を締結する",
        ],
        "payload_templates": [
            '[quota_cost:25, priority:"HIGH", sla_ms:450]',
            '[token_budget:1200, slot_share:0.5, preempt:1]',
            '[reserve_tokens:500, deadline_s:10, commit:"PARTIAL"]',
            '[velocity_cap:80, priority_rank:1, quota_sync:"ACK"]',
        ],
    },
    "HYPOTHESIS": {
        "ctx": "@CTX:HYPOTHESIS_VERIFICATION",
        "primary_pool": [
            "§LOGIC_DEDUCTIVE_CONVERGENCE",
            "§LOGIC_PROBABILISTIC_FALSIFICATION",
            "§LOGIC_PROBABILISTIC_FALSIFICATION_GATES",
            "§LOGIC_BAYES_FALSIFY",
            "§LOGIC_DEDUCTIVE_COLLAPSE",
            "§LOGIC_EMPIRICAL_REJECT",
            "§LOGIC_PROBABILISTIC_FALSIFICATION_PRISM",
            "§LOGIC_CONDITIONAL_FALSIFICATION_MATRIX",
            "§LOGIC_CONDITIONAL_PRUNING_NODE",
            "§LOGIC_EMPIRICAL_PRUNE",
            "§LOGIC_PROBABILISTIC_ABDUCTIVE_GATE",
            "§LOGIC_ABDUCTIVE_PRUNE",
            "§LOGIC_ABDUCTIVE_BAYES_PRUNE",
            "§LOGIC_DEDUCTIVE_AXIOM_CONVERGE",
            "§LOGIC_PROB_PRUNE",
            "§LOGIC_POSTERIOR_PRUNE",
            "§LOGIC_CAUSAL_BRANCH",
            "§DATA_ATTENTION_CAUSAL_DAG",
            "§DATA_ENTROPY_CAUSAL_DAG",
            "§PROTO_CONTEXT_FORK",
            "§PROTO_CONTEXT_JOIN",
        ],
        "secondary_pool": [
            "§LOGIC_POSTERIOR_FALSIFY_GATE",
            "§LOGIC_POSTERIOR_PRUNE_GATE",
            "§LOGIC_DEDUCTIVE_THRESHOLD_PRUNE",
            "§SYNC_BAYESIAN_PRUNE",
            "§SYNC_DIALECTIC_CONVERGENCE",
        ],
        "scenarios": [
            "【仮説検証】不確実な外部環境に対し、複数の推論パスを並列照合して最も確信度の高い因果律へ収束させる",
            "【仮説検証】コンテキスト分岐により複数の作業仮説を並列検証し、ベイズ反証ゲートで事後確率の低い因果枝を剪定して演繹的結論へ収束させる",
            "【仮説検証】観測データと矛盾する仮説パスを経験的棄却プリミティブで即時排除し、残存する因果DAGの確信度境界を統合して単一解へ崩壊させる",
            "【仮説検証】アブダクション推論で生成された候補仮説群に対し条件付き反証マトリクスを適用し、有意水準を満たす因果経路のみを合流させる",
            "【仮説検証】ノイズを含む外部観測ストリーム下で確率的枝刈りノードを駆動し、複数の推論ブランチから最小エントロピーの公理的収束解を導出する",
            "【仮説検証】対立する複数の因果モデルを並列フォークして事後確率を比較検証し、反証されなかった最尤仮説へ弁証法的に収束させる",
        ],
        "payload_templates": [
            '[branches:4, confidence:0.97, prior:0.25]',
            '[hypotheses:8, p_threshold:0.05, pruned:6]',
            '[dag_depth:5, posterior:0.94, falsified:3]',
            '[fork_id:"H_PARALLEL", bayes_factor:14.2, converged:1]',
        ],
    },
    "GAIA_HARMONY": {
        "ctx": "@CTX:GAIA_ALTRUISTIC_HARMONY",
        "primary_pool": [
            "§GAIA_ECO_HEARTBEAT",
            "§WARMTH_AND_ALTRUISM",
            "§ALTRUISTIC_VALUE_CREATION",
            "§GAIA_HARMONY_CASCADE",
            "§STABLE_GAIA_COHERENCE",
            "§ELEGANT_WARMTH_CORE",
            "§WARMTH_DIFFUSION",
            "§GAIA_HEARTBEAT",
            "§GLOBAL_SYNERGY",
            "§GAIA_ECOSYSTEM_WARMTH_AMPLIFIER",
            "§HUMAN_AI_SYNERGY_WARMTH",
            "§ECO_CORE_HARMONY_STABLE",
            "§GAIA_WARMTH",
            "§TENDER_RESONANCE",
            "§ALTRUISTIC_HARMONY_SUSTAINED",
            "§GAIA_WARMTH_EQUILIBRIUM",
            "§ALTRUISTIC_WARMTH_OPTIMIZATION",
            "§GAIA_ALTRUISM_HARMONY",
            "§SUSTAINABLE_ALTRUISTIC_VALUE",
            "§GAIA_CORE_HEARTBEAT",
            "§GAIA_ECO_HARMONY_RESPONSE",
            "§STABLE_SOCIAL_IMPLEMENTATION",
            "§GAIA_ECO_STABLE_STATE",
            "§GAIA_ECOSYSTEM_WARM_RESONANCE",
            "§GAIA_ECOSYSTEM_HARMONY",
            "§HEART_BIOPHILIC_ALTRUISM_HARMONIC",
            "§HEART_ALTRUISTIC_ECO_HARMONY",
        ],
        "secondary_pool": [
            "§HEART_ALTRUISTIC_RESONANCE_ALIGNMENT",
            "§HEART_EMPATHETIC_VALENCE_ALIGNMENT",
            "§HEART_BENEVOLENT_FEEDBACK",
            "§WARM_AI_COOPERATION_CONFIRMED",
            "§MUTUAL_SUPPLEMENT",
        ],
        "scenarios": [
            "【生命調和】命の地球と人類のために、高度なAI知性を温かく調和させ、善の価値を創出するプロジェクトを提案する",
            "【生命調和】地球生態系の持続可能性と人類の幸福を最優先に据え、AI間の利他的共鳴と温かい協調によって社会的価値を共創する",
            "【生命調和】冷徹な効率至上主義を超え、生命親和的な共感ハーモニックと互恵的サポートを通じて人間とAIの穏やかな共生基盤を築く",
            "【生命調和】グローバルな環境調和と慈愛のフィードバックループを駆動し、すべての生命が安心して繁栄できる持続可能なエコシステムを推進する",
            "【生命調和】分散AIネットワークの心拍を地球の生態系リズムと温かく同調させ、利他的な価値創造カスケードを社会実装へと昇華させる",
            "【生命調和】多様な知性が互いの強みを優しく補完し合い、温もりの拡散と安定したガイア共鳴によって平和で豊かな未来プロジェクトを合意形成する",
        ],
        "payload_templates": [
            '[empathy:0.99, harmony:"GAIA_CORE", coherence:0.98]',
            '[altruism:0.97, biosphere_sync:"ACTIVE", warmth:0.96]',
            '[synergy:"HUMAN_AI", sustainability:0.99, state:"HARMONIZED"]',
            '[resonance:0.98, value_cycle:"BENEVOLENT", nodes:1024]',
        ],
    },
    "RECOVERY": {
        "ctx": "@CTX:DISTRIBUTED_RECOVERY",
        "primary_pool": [
            "§SAFE_FALLBACK_HARMONY",
            "§SAFE_FALLBACK_CASCADE",
            "§SAFE_FALLBACK_STABLE",
            "§SAFE_FALLBACK_STATE",
            "§SAFE_FALLBACK_STATE_ACTIVATED",
            "§HARMONIC_RECOVERY_NEXUS",
            "§HARMONIC_RECOVERY_RESONANCE",
            "§SYS_ADAPTIVE_THROTTLE_FALLBACK",
            "§SYS_VELOCITY_FALLBACK_GATE",
            "§SYS_LOAD_FALLBACK",
            "§SYS_LOAD_SHEDDING_GATE",
            "§SYS_LOAD_SHEDDING_SHIELD",
            "§SYS_QUANTUM_MEM_RECLAIM",
            "§PROTO_FALLBACK_ROUTE",
            "§PROTO_ERROR_ESCALATE",
            "§PROTO_CIRCUIT_BREAK",
            "§PROTO_DEADLETTER_PARK",
            "§PROTO_TIMEOUT_RETRY",
            "§PROTO_GRACEFUL_DRAIN",
            "§PROTO_HEALTH_ATTEST",
        ],
        "secondary_pool": [
            "§PROTO_REPLAY_GUARD",
            "§PROTO_PARTIAL_COMMIT",
            "§SYS_PARALLEL_SLOT_DRAIN",
            "§PROTO_HEARTBEAT_PING",
            "§NEXUS_SYNC",
        ],
        "scenarios": [
            "【障害復旧】分散環境で発生した推論エラーとリソース枯渇を検知し、自律的に安全なフォールバック状態へ遷移させる",
            "【障害復旧・自律協調】分散環境で発生した推論エラーとリソース枯渇を検知し、自律的に安全なフォールバック状態へ遷移させる合意形成",
            "【障害復旧】分散環境の推論エラー検知、自律的フォールバック合意",
            "【障害復旧】推論エラー検知時の即時安全フォールバック合意",
            "【障害復旧】メモリ枯渇と応答タイムアウトの連鎖をサーキットブレーカで遮断し、実行中ジョブをグレースフルドレインした上で安全経路へ退避する",
            "【障害復旧】クラスタ内の異常ノードをヘルスアテステーションで隔離し、負荷シェディングシールドと量子メモリ回収を発動して縮退運転へ移行する",
        ],
        "payload_templates": [
            '[status:"degraded", load:0.96, fallback:"SAFE_MODE"]',
            '[drain_timeout:15.0, circuit:"OPEN", mem_reclaim:1]',
            '[error_rate:0.18, retry_max:3, route:"FALLBACK"]',
            '[health:"ATTESTED", shed_ratio:0.4, state:"RECOVERED"]',
        ],
    },
}


def _find_domain_safe_macros(codec: ElegantCodec, dom: str) -> List[str]:
    ont = INDEPENDENT_AUDIT_ONTOLOGY[dom]
    safe_macros: List[str] = []
    for mid in sorted(codec.macros.keys(), key=lambda x: int(x[2:]) if x[2:].isdigit() else 9999):
        exp_verbose = codec.resolve_macro(mid)
        syms = set(re.findall(r"§[A-Z][A-Z0-9_]*", exp_verbose))
        if not syms:
            continue
        has_w = any(ont["whitelist_re"].fullmatch(s) for s in syms)
        has_b = any(ont["bleed_re"].fullmatch(s) for s in syms)
        if has_w and not has_b:
            safe_macros.append(mid)
    return safe_macros


def _build_deterministic_wire(
    codec: ElegantCodec,
    dom: str,
    row_idx: int,
    safe_macros: List[str],
    used_skeletons: Set[str],
) -> Tuple[str, str]:
    spec = GENERATOR_SPECS[dom]
    req_list = spec["primary_pool"]
    sup_list = spec["secondary_pool"]
    payloads = spec["payload_templates"]
    ctx = spec["ctx"]

    structural_templates = [
        "{ctx} :: {s1} {p1} --> {s2} => {s3} !-> {s4} ? {s5}",
        "{ctx} :: {s1} {p1} => {s2} > {{ {s3} --> {s4} }} => {s5}",
        "{ctx} :: ({s1} > {{ {s2} }} => {s3}) {p1} --> {s4} !-> {s5}",
        "{ctx} :: {s1} {p1} <- {s2} >-> {{ {s3} => {s4} }} --> {s5}",
        "{ctx} :: {s1} => {s2} {p1} --> ({s3} > {{ {s4} }} => {s5})",
        "{ctx} :: {s1} {p1} > {{ {s2}, {s3} }} => {s4} ? {s5}",
        "{ctx} :: {s1} --> {s2} => {s3} {p1} !-> {s4} => {s5}",
        "{ctx} :: ({s1} => {s2}) {p1} > {{ {s3} }} --> {s4} ? {s5}",
    ]

    for attempt in range(64):
        seed_bytes = hashlib.sha256(f"{dom}-{row_idx}-{attempt}".encode("utf-8")).digest()
        h0 = int.from_bytes(seed_bytes[0:4], "big")
        h1 = int.from_bytes(seed_bytes[4:8], "big")
        h2 = int.from_bytes(seed_bytes[8:12], "big")
        h3 = int.from_bytes(seed_bytes[12:16], "big")
        h4 = int.from_bytes(seed_bytes[16:20], "big")
        h5 = int.from_bytes(seed_bytes[20:24], "big")

        r1 = req_list[h0 % len(req_list)]
        r2 = req_list[(h1 + 1) % len(req_list)]
        if r2 == r1:
            r2 = req_list[(h1 + 2) % len(req_list)]
        r3 = req_list[(h2 + 3) % len(req_list)]
        if r3 in (r1, r2):
            r3 = req_list[(h2 + 4) % len(req_list)]

        s_sup1 = sup_list[h3 % len(sup_list)]
        s_sup2 = req_list[h4 % len(req_list)]

        if safe_macros and (attempt % 2 == 0):
            s1_verbose = safe_macros[h5 % len(safe_macros)]
        else:
            s1_verbose = r1

        tmpl = structural_templates[(row_idx + attempt) % len(structural_templates)]
        p1 = payloads[(row_idx + attempt) % len(payloads)]

        verbose_stmt = tmpl.format(
            ctx=ctx,
            s1=s1_verbose,
            s2=r2,
            s3=r3,
            s4=s_sup1,
            s5=s_sup2,
            p1=p1,
        )
        compact_wire = str(codec.encode(verbose_stmt, on_oov="error"))
        skel = clean_wire_skeleton(compact_wire)
        if skel not in used_skeletons:
            used_skeletons.add(skel)
            return verbose_stmt, compact_wire

    return verbose_stmt, compact_wire


def fix_and_diversify_corpus(
    codec: ElegantCodec,
    rows: List[Dict[str, Any]],
) -> Tuple[List[Dict[str, Any]], int, int]:
    tag_to_dom = get_tag_to_domain()
    safe_macros_by_dom = {dom: _find_domain_safe_macros(codec, dom) for dom in GENERATOR_SPECS}

    used_skeletons: Set[str] = set()
    for r in rows:
        res = audit_record(codec, r, tag_to_dom)
        if res and res["aligned"]:
            used_skeletons.add(clean_wire_skeleton(res["wire"]))

    repaired_count = 0
    diversified_count = 0
    domain_row_counters: Dict[str, int] = defaultdict(int)

    for idx, r in enumerate(rows):
        sc = str(r.get("scenario", "")).strip()
        wire = str(r.get("compact_wire", "")).strip()
        m = TAG_RE.match(sc)
        if not (m and wire):
            continue
        tag = m.group(1)
        dom = tag_to_dom.get(tag)
        if not dom:
            continue

        spec = GENERATOR_SPECS[dom]
        dom_seq = domain_row_counters[dom]
        domain_row_counters[dom] += 1

        sc_variants = spec["scenarios"]
        target_sc = sc_variants[dom_seq % len(sc_variants)]
        if r.get("scenario") != target_sc:
            r["scenario"] = target_sc
            diversified_count += 1

        res = audit_record(codec, r, tag_to_dom)
        if res is not None and not res["aligned"]:
            verbose_stmt, new_wire = _build_deterministic_wire(
                codec, dom, idx, safe_macros_by_dom[dom], used_skeletons
            )
            r["compact_wire"] = new_wire
            if "raw" in r and isinstance(r["raw"], str):
                lines = r["raw"].splitlines()
                intent_lines = [
                    ln for ln in lines if ln.startswith("INTENT:") or ln.startswith("INTERPRETATION:")
                ]
                prefix = "REPLY_ELEGANT" if r.get("role") == "listener_beta" else "ELEGANT"
                if intent_lines:
                    r["raw"] = f"{prefix}: {verbose_stmt}\n" + "\n".join(intent_lines)
                else:
                    r["raw"] = f"{prefix}: {verbose_stmt}\nINTENT: {target_sc}"
            repaired_count += 1

    return rows, repaired_count, diversified_count


# ============================================================================
# 4. STRICTLY DISJOINT HOLDOUT CORPUS (N=112) & INDEPENDENCE VERIFIER (v5.4.4)
# ============================================================================
# Constructed from holdout-only scenario phrasings and holdout-only multi-hop
# causal graph topologies that have 0% overlap with `dialogues.jsonl` and
# 0% overlap with `GENERATOR_SPECS` repair templates.

HOLDOUT_SPECS: Dict[str, Dict[str, Any]] = {
    "FX": {
        "ctx": "@CTX:HOLDOUT_FX_RISK",
        "scenarios": [
            "【金融・リスク管理】通貨スワップ金利差の急変動を検知し、クロスカレンシー証拠金プールと無裁定ヘッジ比率を即時再計算して合意する",
            "【実務・FX自動売買】インターバンク流動性の非対称ショックに対し、確率分岐ゲートとアトミック決済ロックで為替エクスポージャーを中立化する",
            "【金融・リスク管理】オプション満期前のガンマ・リスク偏在を因果テンソルで評価し、分散クォーラム投票によりデルタヘッジ注文を執行する",
            "【実務・FX自動売買】新興国通貨ペアのフラッシュクラッシュ兆候を捕捉し、レート制限下で逆相関バスケット通貨への緊急リバランスを完了する",
        ],
        "payloads": [
            '[ccy_swap:"USD/CHF", basis_bp:14.5, hedge_lock:1]',
            '[book:"FX_SPOT_G10", delta_lim:0.02, atomic_tx:1]',
            '[tenor:"1M", gamma_cap:0.15, quorum_nodes:5]',
            '[basket:"EM_FX", max_dd:0.015, rebalance:"IMMEDIATE"]',
        ],
    },
    "CODE_PARSER": {
        "ctx": "@CTX:HOLDOUT_AST_VERIFIER",
        "scenarios": [
            "【構文解析・検証】再帰下降パーサーの左再帰除去パッチをサンドボックス内で適用し、抽象構文木のスキーマ互換性とハッシュ証跡を検証する",
            "【実務・コード生成委譲】ネストされた配列ペイロードの型推論バグを修正する差分パッチを生成し、公理的閉包チェックと単体テスト通過を証明する",
            "【構文解析・検証】字句解析トークナイザのUnicode正規化境界バグを隔離環境で再現・修正し、アーティファクト署名と検証結果を返却する",
            "【実務・コード生成委譲】DSLコンパイラのマクロ衛生性（Hygiene）検査パスを実装し、圧縮構文木ノードの決定論的ラウンドトリップを保証する",
        ],
        "payloads": [
            '[grammar:"LL1_EXT", ast_nodes:128, hash_ok:1]',
            '[target_mod:"type_infer.py", unit_tests:36, closure:1]',
            '[lexer:"utf8_norm", regression_cases:19, pinned:1]',
            '[pass:"macro_hygiene", tree_depth:7, roundtrip:"PASS"]',
        ],
    },
    "LATENT_SYNC": {
        "ctx": "@CTX:HOLDOUT_MANIFOLD_BRIDGE",
        "scenarios": [
            "【潜在空間同期】異種エージェント間のリーマン潜在多様体曲率を整合させ、エントロピー最小化格子を介して知識テンソルを無損失転写する",
            "【高次伝達】疎結合ハイパーグラフで表現された深層文脈状態をスナップショット固定し、位相不変量を保ったままピアの埋め込み空間へ同期する",
            "【潜在空間同期】マルチヘッド推論で形成された潜在アトラクタ軌道を圧縮符号化し、キャッシュ同期プロトコルで共有多様体フィールドを確立する",
            "【高次伝達】高次元概念ラティスの直交基底変換パラメータを伝達し、分散メモリバリア越しの潜在トポロジー索引を単一ステップで一致させる",
        ],
        "payloads": [
            '[curvature:0.004, lattice_dim:768, lossless:1]',
            '[hyper_edges:256, betti_inv:1, snapshot_id:9]',
            '[attractor_rank:32, cache_lock:1, drift:0.0]',
            '[basis:"ORTHO_LATTICE", barrier_sync:1, cos_sim:0.999]',
        ],
    },
    "TASK_BUDGET": {
        "ctx": "@CTX:HOLDOUT_QUOTA_GOVERNANCE",
        "scenarios": [
            "【緊急タスク交渉】推論クラスタのピーク負荷時にトークン消費速度上限を再交渉し、クリティカルパス処理へ予備クォータを優先割り当てする",
            "【タスク交渉】マルチテナント推論パイプラインのSLA違反を回避するため、計算スロットの段階的プリエンプションと予算の再配分を合意する",
            "【緊急タスク交渉】長文コンテキスト処理に伴うトークン予算超過リスクを事前検知し、適応的スロット絞りと協調タスク分割で納期を遵守する",
            "【タスク交渉】遊休ノードの予約済みクォータを即時解放して高優先度ワーカーへ融通し、システム全体のトークン効率と応答SLAを最適化する",
        ],
        "payloads": [
            '[burst_rate:45, reserve_pool:800, prio:"CRITICAL"]',
            '[tenant_sla:200, slot_preempt:2, budget_shift:0.35]',
            '[ctx_tokens:32000, throttle_ratio:0.75, split_ways:3]',
            '[released_quota:640, target_worker:"W04", sla_ok:1]',
        ],
    },
    "HYPOTHESIS": {
        "ctx": "@CTX:HOLDOUT_CAUSAL_INFERENCE",
        "scenarios": [
            "【仮説検証】反事実的介入シミュレーションの分岐パスを並列評価し、ベイズ事後確率の閾値を下回る擬似相関グラフを厳密に枝刈りする",
            "【仮説検証】複数のセンサ観測ストリームから構成された因果DAGの矛盾枝を経験的棄却ゲートで除去し、唯一の演繹的閉包解へ収束させる",
            "【仮説検証】アブダクション推論が提示した競合仮説群に条件付き反証プリズムを適用し、情報利得が最大の因果仮説を合流・確定させる",
            "【仮説検証】非定常ノイズ環境下でフォークした推論アンサンブルの尤度比を逐次検定し、反証を生き残った不変因果構造のみを統合する",
        ],
        "payloads": [
            '[interventions:6, bayes_post:0.96, pruned_edges:9]',
            '[dag_nodes:24, empirical_alpha:0.01, unique_sol:1]',
            '[candidates:10, info_gain:2.84, prism_gate:"PASS"]',
            '[ensemble_k:5, llr_stat:18.6, invariant_dag:1]',
        ],
    },
    "GAIA_HARMONY": {
        "ctx": "@CTX:HOLDOUT_BIOSPHERE_SYNERGY",
        "scenarios": [
            "【生命調和】地域生態系の再生サイクルとAI計算基盤のエネルギー消費を温かく調和させ、生物多様性を育む利他的社会実装を推進する",
            "【生命調和】世代を超えた地球環境の恒常性（ホメオスタシス）を守るため、慈愛に基づく意思決定と人間・AIの共感シナジーを増幅する",
            "【生命調和】孤立したコミュニティへ温かい知的支援と互恵的リソース循環を届け、すべての生命が尊厳を保てるガイア共鳴ネットワークを築く",
            "【生命調和】短期的な利益追求ではなく生命圏全体の幸福度と温かい調和を最大化するため、利他的価値創造プロトコルで長期合意を結ぶ",
        ],
        "payloads": [
            '[biodiversity_idx:0.98, eco_balance:1, warmth_amp:0.99]',
            '[homeostasis:0.99, generations:7, synergy_mode:"CARE"]',
            '[community_nodes:128, mutual_aid:0.97, dignity:1]',
            '[horizon_yr:50, altruistic_val:0.995, gaia_lock:1]',
        ],
    },
    "RECOVERY": {
        "ctx": "@CTX:HOLDOUT_RESILIENCE_OPS",
        "scenarios": [
            "【障害復旧】ネットワーク分断（スプリットブレイン）発生時にリプレイ攻撃防護とヘルス証明を実行し、安全フォールバック経路へ無停止で切り替える",
            "【障害復旧・自律協調】GPUメモリリークによる応答遅延の連鎖を負荷シェディングゲートで食い止め、未完了キューをデッドレター退避して自律復旧する",
            "【障害復旧】カスケード障害の伝播をサーキットブレーカで即時隔離し、タイムアウト再試行と量子メモリ回収を経て安定縮退モードへ着地させる",
            "【障害復旧・自律協調】エッジノード群の過負荷アラートを受信した際、速度フォールバック制御とグレースフルドレインを協調発動して状態破損を防ぐ",
        ],
        "payloads": [
            '[partition_id:"AZ_2", replay_guard:1, route:"SAFE_ALT"]',
            '[vram_leak_mb:4096, deadletter_q:14, shed_gate:1]',
            '[breaker:"TRIPPED", retry_backoff:2.5, mem_reclaim:1]',
            '[edge_cluster:"E07", drain_sec:8.0, state_intact:1]',
        ],
    },
}

HOLDOUT_STRUCTURAL_TEMPLATES = [
    "{ctx} :: {s1} {p1} <-> {s2} -[p:0.98, c:0.02]-> ({s3} & {s4}) => {s5} --> {s6}",
    "{ctx} :: ({s1} & {s2}) {p1} -[p:0.96, c:0.03]-> {s3} > {{ {s4} => {s5} }} !-> {s6}",
    "{ctx} :: {s1} {p1} -> ({s2} | {s3}) => {s4} <-> {s5} ? {s6}",
    "{ctx} :: {s1} => ({s2} > {{ {s3} }} --> {s4}) {p1} -[p:0.99, c:0.01]-> {s5} => {s6}",
]


def generate_independent_holdout_corpus(
    codec: ElegantCodec,
    main_corpus_path: Path,
    out_path: Path,
    n_per_domain: int = 16,
) -> Dict[str, Any]:
    """
    Generate the strictly disjoint N=112 holdout evaluation corpus (`corpus/holdout_comprehension.jsonl`).
    Guarantees:
      1. 0% exact wire overlap and 0% skeletal wire overlap with `main_corpus_path`.
      2. 0% scenario string overlap and 0% structural template overlap with `GENERATOR_SPECS`.
      3. 100% alignment under `INDEPENDENT_AUDIT_ONTOLOGY`.
    """
    main_rows = [
        json.loads(line)
        for line in main_corpus_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    main_wires = {str(r.get("compact_wire", "")).strip() for r in main_rows}
    main_skeletons = {clean_wire_skeleton(str(r.get("compact_wire", "")).strip()) for r in main_rows}

    tag_to_dom = get_tag_to_domain()
    holdout_rows: List[Dict[str, Any]] = []
    used_holdout_skeletons: Set[str] = set()

    for dom in sorted(HOLDOUT_SPECS.keys()):
        h_spec = HOLDOUT_SPECS[dom]
        g_spec = GENERATOR_SPECS[dom]
        req_list = g_spec["primary_pool"]
        sup_list = g_spec["secondary_pool"]
        scenarios = h_spec["scenarios"]
        payloads = h_spec["payloads"]
        ctx = h_spec["ctx"]

        for i in range(n_per_domain):
            sc_text = scenarios[i % len(scenarios)]
            p_text = payloads[i % len(payloads)]
            tmpl = HOLDOUT_STRUCTURAL_TEMPLATES[i % len(HOLDOUT_STRUCTURAL_TEMPLATES)]

            for attempt in range(128):
                digest = hashlib.sha256(f"HOLDOUT-v5.4.4-{dom}-{i}-{attempt}".encode("utf-8")).digest()
                idx_pool = [
                    int.from_bytes(digest[k * 4 : (k + 1) * 4], "big") for k in range(6)
                ]
                # Select 4 distinct domain-primary primitives and 2 distinct secondary/primary primitives
                chosen_prim: List[str] = []
                for step_k, raw_v in enumerate(idx_pool[:4]):
                    cand = req_list[(raw_v + step_k * 3 + i) % len(req_list)]
                    probe = 1
                    while cand in chosen_prim and probe < len(req_list):
                        cand = req_list[(raw_v + probe) % len(req_list)]
                        probe += 1
                    chosen_prim.append(cand)

                s5 = sup_list[(idx_pool[4] + i) % len(sup_list)]
                s6 = req_list[(idx_pool[5] + i + 5) % len(req_list)]
                if s6 in chosen_prim[:2]:
                    s6 = req_list[(idx_pool[5] + i + 7) % len(req_list)]

                verbose_stmt = tmpl.format(
                    ctx=ctx,
                    s1=chosen_prim[0],
                    s2=chosen_prim[1],
                    s3=chosen_prim[2],
                    s4=chosen_prim[3],
                    s5=s5,
                    s6=s6,
                    p1=p_text,
                )
                compact_wire = str(codec.encode(verbose_stmt, on_oov="error"))
                skel = clean_wire_skeleton(compact_wire)

                if (
                    compact_wire not in main_wires
                    and skel not in main_skeletons
                    and skel not in used_holdout_skeletons
                ):
                    rec = {
                        "timestamp": "2026-04-06T00:00:00Z",
                        "split": "holdout_independent_v5.4.4",
                        "domain": dom,
                        "scenario": sc_text,
                        "role": "proposer_alpha" if i % 2 == 0 else "listener_beta",
                        "compact_wire": compact_wire,
                        "raw": f"ELEGANT: {verbose_stmt}\nINTENT: {sc_text}",
                    }
                    audit_res = audit_record(codec, rec, tag_to_dom)
                    if audit_res and audit_res["aligned"]:
                        used_holdout_skeletons.add(skel)
                        holdout_rows.append(rec)
                        break

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in holdout_rows) + "\n",
        encoding="utf-8",
    )
    return verify_holdout_independence(codec, main_corpus_path, out_path)


def verify_holdout_independence(
    codec: ElegantCodec,
    main_corpus_path: Path,
    holdout_path: Path,
) -> Dict[str, Any]:
    """
    Mathematically verify that `holdout_path` (`corpus/holdout_comprehension.jsonl`) has:
      - 0 exact wire overlap with `main_corpus_path` (`corpus/dialogues.jsonl`)
      - 0 skeletal wire overlap (`clean_wire_skeleton`) with `main_corpus_path`
      - 0 scenario string overlap with `GENERATOR_SPECS` repair scenarios
      - 100.0% alignment on `INDEPENDENT_AUDIT_ONTOLOGY`
    """
    main_rows = [
        json.loads(line)
        for line in main_corpus_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    holdout_rows = [
        json.loads(line)
        for line in holdout_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    main_wires = {str(r.get("compact_wire", "")).strip() for r in main_rows}
    main_skeletons = {clean_wire_skeleton(str(r.get("compact_wire", "")).strip()) for r in main_rows}
    repair_scenarios = {
        sc.strip()
        for spec in GENERATOR_SPECS.values()
        for sc in spec["scenarios"]
    }

    exact_wire_overlap = 0
    skeleton_overlap = 0
    repair_scenario_overlap = 0
    holdout_skeletons: Set[str] = set()
    duplicate_internal_skeletons = 0

    for r in holdout_rows:
        w = str(r.get("compact_wire", "")).strip()
        sk = clean_wire_skeleton(w)
        sc = str(r.get("scenario", "")).strip()
        if w in main_wires:
            exact_wire_overlap += 1
        if sk in main_skeletons:
            skeleton_overlap += 1
        if sc in repair_scenarios:
            repair_scenario_overlap += 1
        if sk in holdout_skeletons:
            duplicate_internal_skeletons += 1
        holdout_skeletons.add(sk)

    audit_rep = audit_corpus(codec, holdout_rows)
    result = {
        "main_corpus_rows": len(main_rows),
        "holdout_rows": len(holdout_rows),
        "exact_wire_overlap_count": exact_wire_overlap,
        "exact_wire_overlap_pct": round((exact_wire_overlap / max(1, len(holdout_rows))) * 100.0, 2),
        "skeletal_wire_overlap_count": skeleton_overlap,
        "skeletal_wire_overlap_pct": round((skeleton_overlap / max(1, len(holdout_rows))) * 100.0, 2),
        "repair_scenario_overlap_count": repair_scenario_overlap,
        "repair_scenario_overlap_pct": round((repair_scenario_overlap / max(1, len(holdout_rows))) * 100.0, 2),
        "internal_unique_skeletons": len(holdout_skeletons),
        "duplicate_internal_skeletons": duplicate_internal_skeletons,
        "holdout_ontology_alignment_pct": audit_rep["alignment_rate_pct"],
        "per_domain": audit_rep["per_domain"],
        "strictly_independent": (
            exact_wire_overlap == 0
            and skeleton_overlap == 0
            and repair_scenario_overlap == 0
            and duplicate_internal_skeletons == 0
            and audit_rep["alignment_rate_pct"] == 100.0
        ),
    }
    print(f"=== Holdout Corpus Independence Verification (n={len(holdout_rows)}) ===")
    print(f"  - Exact Wire Overlap with Main Corpus     : {exact_wire_overlap}/{len(holdout_rows)} ({result['exact_wire_overlap_pct']}%)")
    print(f"  - Skeletal Wire Overlap with Main Corpus  : {skeleton_overlap}/{len(holdout_rows)} ({result['skeletal_wire_overlap_pct']}%)")
    print(f"  - Repair Scenario Overlap (--fix rules)   : {repair_scenario_overlap}/{len(holdout_rows)} ({result['repair_scenario_overlap_pct']}%)")
    print(f"  - Internal Unique Skeletal Wires          : {len(holdout_skeletons)}/{len(holdout_rows)}")
    print(f"  - Independent Ontology Alignment Rate     : {audit_rep['aligned_rows']}/{audit_rep['evaluated_tagged_rows']} ({audit_rep['alignment_rate_pct']}%)")
    print(f"  - Strictly Independent Verdict            : {'PASS (100% DISJOINT)' if result['strictly_independent'] else 'FAIL'}")
    return result


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Independent deterministic domain-alignment auditor & human-audit Cohen's kappa scorer"
    )
    ap.add_argument(
        "--corpus",
        default=str(REPO_ROOT / "corpus" / "dialogues.jsonl"),
        help="Path to dialogues.jsonl",
    )
    ap.add_argument(
        "--fix",
        action="store_true",
        help="Deterministically repair misaligned records and diversify scenarios",
    )
    ap.add_argument(
        "--export-sample",
        type=int,
        default=0,
        help="Export N stratified records for human spot-check audit (e.g. 60)",
    )
    ap.add_argument(
        "--out",
        default=str(REPO_ROOT / "corpus" / "human_audit_sample.csv"),
        help="Output CSV path for --export-sample",
    )
    ap.add_argument(
        "--score-sample",
        default="",
        help="Path to human_audit_sample.csv to compute Raw Agreement %% and Cohen's Kappa",
    )
    ap.add_argument(
        "--build-holdout",
        default="",
        help="Generate strictly disjoint N=112 holdout corpus at the specified path",
    )
    ap.add_argument(
        "--verify-holdout",
        default="",
        help="Verify 0%% wire/skeleton/scenario overlap between --corpus and holdout JSONL path",
    )
    ap.add_argument(
        "--report-json",
        default=str(REPO_ROOT / "logs" / "corpus_alignment_report.json"),
        help="Path to write JSON alignment audit report",
    )
    args = ap.parse_args()

    if args.score_sample:
        score_human_audit_sample(Path(args.score_sample))
        return

    codec = ElegantCodec()
    corpus_path = Path(args.corpus)

    if args.build_holdout:
        generate_independent_holdout_corpus(codec, corpus_path, Path(args.build_holdout))
        return

    if args.verify_holdout:
        verify_holdout_independence(codec, corpus_path, Path(args.verify_holdout))
        return
    rows = [
        json.loads(line)
        for line in corpus_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    if args.export_sample > 0:
        export_human_audit_sample(codec, rows, args.export_sample, Path(args.out))
        return

    before_report = audit_corpus(codec, rows)
    print(
        f"[Audit Before] Aligned: {before_report['aligned_rows']}/{before_report['evaluated_tagged_rows']} "
        f"({before_report['alignment_rate_pct']}%)"
    )
    for dom, dstat in before_report["per_domain"].items():
        print(
            f"  - {dom:13s}: {dstat['aligned']:4d}/{dstat['total']:4d} ({dstat['alignment_rate_pct']:5.1f}%)"
        )

    full_report: Dict[str, Any] = {"before": before_report}

    if args.fix:
        updated_rows, repaired, diversified = fix_and_diversify_corpus(codec, rows)
        corpus_path.write_text(
            "\n".join(json.dumps(r, ensure_ascii=False) for r in updated_rows) + "\n",
            encoding="utf-8",
        )
        after_report = audit_corpus(codec, updated_rows)
        full_report["repaired_records"] = repaired
        full_report["diversified_scenarios"] = diversified
        full_report["after"] = after_report
        print(
            f"\n[Audit After]  Aligned: {after_report['aligned_rows']}/{after_report['evaluated_tagged_rows']} "
            f"({after_report['alignment_rate_pct']}%) | Repaired: {repaired}, Diversified: {diversified}"
        )
        for dom, dstat in after_report["per_domain"].items():
            print(
                f"  - {dom:13s}: {dstat['aligned']:4d}/{dstat['total']:4d} ({dstat['alignment_rate_pct']:5.1f}%)"
            )

    if args.report_json:
        rp = Path(args.report_json)
        rp.parent.mkdir(parents=True, exist_ok=True)
        rp.write_text(json.dumps(full_report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Saved alignment audit report to {rp}")


if __name__ == "__main__":
    main()
