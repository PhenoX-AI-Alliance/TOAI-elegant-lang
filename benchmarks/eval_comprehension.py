#!/usr/bin/env python3
"""
TOAI-elegant-lang Receiver-Comprehension Evaluation Harness (v5.4.3)
====================================================================
Rigorous 4-choice blind evaluation harness measuring whether a receiver LLM
can recover the human intent (`scenario`) behind a TOAI-elegant-lang wire message.

Experimental Hygiene & Controls (v5.4.3):
  - Five Experimental Conditions (A-E):
      * A (Compact Wire Only)     : Raw Demotic codes (§S01, §X238...); @CTX & [k:v] stripped.
      * B (Sacred Verbose Names)  : Decoded & macro-expanded Sacred symbol names; @CTX & [k:v] stripped.
      * C (Sacred + Rosetta Defs) : Condition B + Rosetta lexicon definitions for each symbol.
      * D (Shuffle Control)       : Condition B syntax skeleton preserved, but symbol names randomly
                                    permuted across messages (tests whether symbol semantics carry meaning
                                    beyond structural operators).
      * E (Plaintext Upper Bound) : Concise natural-language operational summary of the message
                                    (upper-bound reference).
  - Strict Separation of `--keep-ctx` (Protocol Header Mode):
      * Because `@CTX:DOMAIN` and payload keys (`[pair:*, module:*]`) explicitly reveal domain cues,
        `--keep-ctx` is isolated into separate files (`*_ctx.*`) and reported separately from blind A-E.
  - Statistical Rigor:
      * Wilson 95% confidence intervals (`wilson(k, n)`).
      * Paired McNemar test (`mcnemar_test`) with exact binomial p-value & continuity-corrected chi2
        for comparing conditions on identical items (e.g. A vs B, B vs D, B vs C).
      * Option-position bias mitigation (`--rotate-options`) and chosen-letter (A-D) histogram.
  - Stratified & Cost-Efficiency Metrics:
      * Micro accuracy, Macro accuracy across scenarios/domains, and explicit separation of
        "Disaster Recovery (Routine Pattern)" vs. "Non-Recovery Domains (FX, Parser, Latent, Budget, etc.)".
      * Prompt character & BPE token counts (`o200k_base`) and Accuracy Gain per 1,000 Tokens.
  - Multi-Backend Zero-Temperature Runner (`run` mode):
      * Supports `ollama`, `anthropic`, `openai`, `gemini` with strict `temperature=0`, minimal `max_tokens`,
        unparseable responses scored as incorrect (`INVALID`), and full raw output persistence.
"""

import argparse
import json
import math
import os
import random
import re
import sys
import time
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from src.codec import ElegantCodec, count_bpe_tokens

TAG = re.compile(r"^【([^】]+)】\s*")
BRACKET = re.compile(r"\[[^\]]*\]")
CTX = re.compile(r"@CTX:\S+")
LETTERS = "ABCD"
VALID_CONDS = ("A", "B", "C", "D", "E")


def clean_wire(w: str) -> str:
    """Strip @CTX:... and [k:v] payloads completely (Skeletal Blind Mode)."""
    return re.sub(r"\s+", " ", BRACKET.sub("", CTX.sub("", w))).strip()


def mask_wire_keep_ctx(w: str) -> str:
    """
    Protocol Header Mode (--keep-ctx):
    Retains `@CTX:DOMAIN` and payload parameter key names while masking literal values to `*`
    (e.g. `[pair:*, limit:*]`). Kept strictly separate from blind Conditions A-E.
    """
    def _mask_bracket(m: re.Match) -> str:
        inner = m.group(0)[1:-1].strip()
        if not inner:
            return "[]"
        keys = []
        for seg in ElegantCodec._split_top_level_comma(inner):
            parsed = ElegantCodec._parse_kv_item(seg)
            if parsed is not None:
                keys.append(f"{parsed[0]}:*")
        return "[" + ", ".join(keys) + "]" if keys else "[]"

    return re.sub(r"\s+", " ", BRACKET.sub(_mask_bracket, w)).strip()


def clean_scn(s: str) -> str:
    return re.sub(r"\s+", " ", BRACKET.sub("", CTX.sub("", TAG.sub("", s))).replace(" ::", "")).strip()


def has_plain_words(w: str) -> bool:
    """True if, after removing §codes and payloads, readable words remain (they would leak the answer)."""
    return bool(re.search(r"[A-Za-z]{4,}", re.sub(r"§\w+", "", clean_wire(w))))


def is_recovery_tag(tag: str) -> bool:
    return "障害復旧" in tag or "RECOVERY" in tag.upper()


def related(t1: str, t2: str) -> bool:
    return t1 == t2 or t1 in t2 or t2 in t1


def load_items(codec: ElegantCodec) -> List[Dict[str, Any]]:
    """Load all corpus records with a tagged scenario and >=2 distinct wire codes and no plain-word leaks."""
    corpus_file = ROOT / "corpus" / "dialogues.jsonl"
    rows = [json.loads(l) for l in corpus_file.read_text(encoding="utf-8").splitlines() if l.strip()]
    seen_w, items = set(), []
    for idx, r in enumerate(rows):
        w, sc = r.get("compact_wire", ""), r.get("scenario", "")
        m = TAG.match(sc)
        if not (w and w.count("§") >= 2 and sc and m) or has_plain_words(w):
            continue
        cw = clean_wire(w)
        if cw in seen_w or len(cw.replace("§", "")) < 4:
            continue
        seen_w.add(cw)
        items.append(
            dict(
                row_id=idx,
                wire=w,
                scenario=clean_scn(sc),
                tag=m.group(1),
            )
        )
    return items


def select_stratified_items(items: List[Dict[str, Any]], n: int, seed: int) -> List[Dict[str, Any]]:
    """Deterministically sample `n` items stratified evenly across distinct scenarios."""
    rng = random.Random(seed)
    by_scn = defaultdict(list)
    for it in items:
        by_scn[it["scenario"]].append(it)
    scns = sorted(by_scn)
    per = max(1, -(-n // max(1, len(scns))))
    chosen = []
    for sc in scns:
        chosen += rng.sample(by_scn[sc], min(per, len(by_scn[sc])))
    rng.shuffle(chosen)
    return chosen[:n]


def build_shuffle_pool(codec: ElegantCodec, chosen_items: List[Dict[str, Any]], seed: int) -> Dict[int, Dict[str, str]]:
    """
    For Condition D (Shuffle Control):
    Collect all decoded Sacred symbols across `chosen_items`, shuffle them deterministically
    using `seed`, and map each item's symbols to random symbols drawn from OTHER messages.
    Preserves exact operator/bracket syntax while breaking symbol-name semantics.
    """
    rng = random.Random(f"shuffle-control-{seed}")
    item_syms: List[List[str]] = []
    all_unique_syms: List[str] = []
    seen = set()
    for it in chosen_items:
        dec = clean_wire(codec.decode(it["wire"], expand_macros=True))
        syms = re.findall(r"§[A-Z][A-Z0-9_]*", dec)
        item_syms.append(syms)
        for s in syms:
            if s not in seen:
                seen.add(s)
                all_unique_syms.append(s)

    if len(all_unique_syms) < 2:
        all_unique_syms = sorted(codec.definitions.keys())

    mapping_per_item: Dict[int, Dict[str, str]] = {}
    for idx, syms in enumerate(item_syms):
        own_set = set(syms)
        candidates = [s for s in all_unique_syms if s not in own_set]
        if len(candidates) < len(own_set):
            candidates = [s for s in sorted(codec.definitions.keys()) if s not in own_set]
        shuffled_cands = rng.sample(candidates, min(len(candidates), max(1, len(own_set))))
        sub_map: Dict[str, str] = {}
        for j, orig_s in enumerate(sorted(own_set)):
            sub_map[orig_s] = shuffled_cands[j % len(shuffled_cands)]
        mapping_per_item[idx] = sub_map
    return mapping_per_item


def synthesize_plaintext_upper_bound(codec: ElegantCodec, wire: str) -> str:
    """
    Condition E (Plaintext Upper Bound):
    Synthesizes a concise natural-language operational description from the lexicon's
    English & Japanese primitive definitions without copying the target `scenario` string.
    """
    dec = clean_wire(codec.decode(wire, expand_macros=True))
    syms = []
    for s in re.findall(r"§[A-Z][A-Z0-9_]*", dec):
        if s in codec.definitions and s not in syms:
            syms.append(s)
    clauses = []
    for s in syms[:4]:
        info = codec.definitions[s]
        ja = info.get("japanese", "").strip()
        en = info.get("definition", "").strip()
        if ja:
            first_sent = ja.split("。")[0].strip()
            clauses.append(first_sent)
        elif en:
            clauses.append(en[:90])
    if not clauses:
        return dec
    return " / ".join(clauses)


def render(
    codec: ElegantCodec,
    wire: str,
    cond: str,
    keep_ctx: bool = False,
    shuffle_map: Optional[Dict[str, str]] = None,
) -> Tuple[str, str]:
    """
    Render `(message_body, glossary_block)` for Conditions A, B, C, D, E.
    """
    cleaner = mask_wire_keep_ctx if keep_ctx else clean_wire

    if cond == "A":
        return cleaner(wire), ""

    dec = cleaner(codec.decode(wire, expand_macros=True))

    if cond == "B":
        return dec, ""

    if cond == "C":
        syms, gl = [], []
        for s in re.findall(r"§[A-Z][A-Z0-9_]*", dec):
            if s in codec.definitions and s not in syms:
                syms.append(s)
        for s in syms[:6]:
            d_en = codec.definitions[s].get("definition", "")[:140]
            gl.append(f"  {s}: {d_en}")
        return dec, ("GLOSSARY:\n" + "\n".join(gl) + "\n") if gl else ""

    if cond == "D":
        smap = shuffle_map or {}
        shuffled_dec = re.sub(
            r"§[A-Z][A-Z0-9_]*",
            lambda m: smap.get(m.group(0), m.group(0)),
            dec,
        )
        return shuffled_dec, ""

    if cond == "E":
        pt = synthesize_plaintext_upper_bound(codec, wire)
        if keep_ctx:
            m_ctx = CTX.search(wire)
            if m_ctx:
                pt = f"{m_ctx.group(0)} :: {pt}"
        return pt, ""

    raise ValueError(f"Unsupported condition: {cond}")


def file_suffix(cond: str, keep_ctx: bool = False, rotate_options: bool = False) -> str:
    suf = cond
    if keep_ctx:
        suf += "_ctx"
    if rotate_options:
        suf += "_rot"
    return suf


def build_for_condition(
    codec: ElegantCodec,
    items: List[Dict[str, Any]],
    chosen: List[Dict[str, Any]],
    cond: str,
    seed: int,
    out_dir: Path,
    keep_ctx: bool = False,
    rotate_options: bool = False,
) -> Dict[str, Any]:
    """Build question markdown and hidden key/metadata JSON for a single condition."""
    shuffle_pool = build_shuffle_pool(codec, chosen, seed) if cond == "D" else {}
    qs: List[str] = []
    key: Dict[str, str] = {}
    meta_questions: Dict[str, Dict[str, Any]] = {}

    for i, it in enumerate(chosen, 1):
        # Distractor selection depends only on (seed, question_index) so identical distractors
        # are paired across Conditions A-E for valid McNemar paired testing.
        r_dist = random.Random(f"{seed}-distractors-{i}")
        tags = sorted({x["tag"] for x in items if not related(x["tag"], it["tag"])})
        picked = []
        for t in r_dist.sample(tags, len(tags)):
            if all(not related(t, q) for q in picked):
                picked.append(t)
            if len(picked) == 3:
                break
        distractors = [
            r_dist.choice(sorted({x["scenario"] for x in items if x["tag"] == t}))
            for t in picked
        ]
        base_opts = distractors + [it["scenario"]]
        r_order = random.Random(f"{seed}-order-{i}")
        r_order.shuffle(base_opts)

        msg, gloss = render(
            codec,
            it["wire"],
            cond,
            keep_ctx=keep_ctx,
            shuffle_map=shuffle_pool.get(i - 1),
        )

        rotations = [0, 1, 2, 3] if rotate_options else [0]
        for rot in rotations:
            opts = base_opts[rot:] + base_opts[:rot]
            qid = f"Q{i}_R{rot}" if rotate_options else f"Q{i}"
            ans_letter = LETTERS[opts.index(it["scenario"])]
            key[qid] = ans_letter
            q_text = (
                f"{qid}\nMESSAGE: {msg}\n{gloss}"
                + "\n".join(f"{L}) {o}" for L, o in zip(LETTERS, opts))
            )
            qs.append(q_text)
            tok_info = count_bpe_tokens(q_text, "o200k_base")
            meta_questions[qid] = {
                "base_qid": f"Q{i}",
                "rotation": rot,
                "answer": ans_letter,
                "tag": it["tag"],
                "is_recovery": is_recovery_tag(it["tag"]),
                "scenario": it["scenario"],
                "prompt_chars": len(q_text),
                "prompt_bpe_tokens": tok_info["tokens"],
            }

    suf = file_suffix(cond, keep_ctx=keep_ctx, rotate_options=rotate_options)
    out_dir.mkdir(parents=True, exist_ok=True)
    q_path = out_dir / f"questions_{suf}.md"
    k_path = out_dir / f"key_{suf}.json"
    m_path = out_dir / f"meta_{suf}.json"

    full_md = "\n\n".join(qs) + "\n"
    q_path.write_text(full_md, encoding="utf-8")
    k_path.write_text(json.dumps(key, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    total_bpe = sum(v["prompt_bpe_tokens"] for v in meta_questions.values())
    total_chars = sum(v["prompt_chars"] for v in meta_questions.values())
    meta_payload = {
        "condition": cond,
        "keep_ctx": keep_ctx,
        "protocol_mode": "protocol_header_keep_ctx" if keep_ctx else "skeletal_blind",
        "rotate_options": rotate_options,
        "seed": seed,
        "n_base_questions": len(chosen),
        "n_total_prompts": len(qs),
        "total_prompt_chars": total_chars,
        "total_prompt_bpe_tokens": total_bpe,
        "mean_prompt_bpe_tokens": round(total_bpe / max(1, len(qs)), 2),
        "questions": meta_questions,
    }
    m_path.write_text(json.dumps(meta_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return meta_payload


def build(a: argparse.Namespace) -> None:
    codec = ElegantCodec()
    items = load_items(codec)
    chosen = select_stratified_items(items, a.n, a.seed)
    scns = sorted({it["scenario"] for it in items})
    out_dir = Path(a.out)

    conds = list(VALID_CONDS) if a.cond == "ALL" else [a.cond]
    for c in conds:
        meta = build_for_condition(
            codec,
            items,
            chosen,
            c,
            a.seed,
            out_dir,
            keep_ctx=getattr(a, "keep_ctx", False),
            rotate_options=getattr(a, "rotate_options", False),
        )
        mode_tag = " [Protocol Header Mode --keep-ctx]" if meta["keep_ctx"] else " [Blind Skeletal Mode]"
        print(
            f"{len(items)} usable records, {len(scns)} distinct scenarios; "
            f"wrote {meta['n_total_prompts']} questions for cond {c}{mode_tag} "
            f"(mean {meta['mean_prompt_bpe_tokens']} BPE tokens/question)"
        )


def wilson(k: int, n: int, z: float = 1.96) -> Tuple[float, float]:
    """Wilson score 95% confidence interval for binomial proportion k/n."""
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0.0, c - h), min(1.0, c + h)


def mcnemar_test(correct_a: List[bool], correct_b: List[bool]) -> Dict[str, Any]:
    """
    Paired McNemar test between two conditions evaluated on the same N questions.
      - n11: both correct
      - n10 (b): Cond 1 correct, Cond 2 wrong
      - n01 (c): Cond 1 wrong, Cond 2 correct
      - n00: both wrong
    Returns exact two-sided binomial p-value and continuity-corrected chi2 statistic.
    """
    if len(correct_a) != len(correct_b):
        raise ValueError("Paired lists must have identical length for McNemar test.")
    n11 = sum(1 for a, b in zip(correct_a, correct_b) if a and b)
    n10 = sum(1 for a, b in zip(correct_a, correct_b) if a and not b)
    n01 = sum(1 for a, b in zip(correct_a, correct_b) if not a and b)
    n00 = sum(1 for a, b in zip(correct_a, correct_b) if not a and not b)

    b, c = n10, n01
    discordant = b + c
    if discordant == 0:
        return {
            "n": len(correct_a),
            "n11_both_correct": n11,
            "b_only_first_correct": b,
            "c_only_second_correct": c,
            "n00_both_wrong": n00,
            "chi2_cc": 0.0,
            "p_value_exact": 1.0,
            "significant_p05": False,
        }

    chi2_cc = ((abs(b - c) - 1.0) ** 2) / discordant if discordant > 0 else 0.0
    k_min = min(b, c)
    # Exact two-sided binomial tail probability under H0: p = 0.5
    tail_prob = sum(math.comb(discordant, i) for i in range(k_min + 1)) * (0.5 ** discordant)
    p_exact = min(1.0, 2.0 * tail_prob)

    return {
        "n": len(correct_a),
        "n11_both_correct": n11,
        "b_only_first_correct": b,
        "c_only_second_correct": c,
        "n00_both_wrong": n00,
        "chi2_cc": round(chi2_cc, 4),
        "p_value_exact": round(p_exact, 6),
        "significant_p05": bool(p_exact < 0.05),
    }


def parse_choice_letter(raw_val: Any) -> str:
    """Strictly parse a single option letter A-D; return 'INVALID' on parse failure."""
    if raw_val is None:
        return "INVALID"
    s = str(raw_val).strip().upper()
    if not s:
        return "INVALID"
    # Match standalone A/B/C/D at start or after Answer:
    m = re.match(r"^(?:ANSWER\s*[:\-]?\s*)?([ABCD])(?![A-Z])", s)
    if m:
        return m.group(1)
    if s[0] in LETTERS and (len(s) == 1 or not s[1].isalpha()):
        return s[0]
    return "INVALID"


def evaluate_answers(
    out_dir: Path,
    cond: str,
    answers_path: Path,
    keep_ctx: bool = False,
    rotate_options: bool = False,
) -> Dict[str, Any]:
    """Compute comprehensive stratified accuracy, Wilson CIs, option bias histogram, and token efficiency."""
    suf = file_suffix(cond, keep_ctx=keep_ctx, rotate_options=rotate_options)
    key_file = out_dir / f"key_{suf}.json"
    meta_file = out_dir / f"meta_{suf}.json"

    if not key_file.is_file() and (out_dir / f"key_{cond}.json").is_file():
        key_file = out_dir / f"key_{cond}.json"
        meta_file = out_dir / f"meta_{cond}.json"

    key: Dict[str, str] = json.loads(key_file.read_text(encoding="utf-8"))
    raw_ans_data = json.loads(answers_path.read_text(encoding="utf-8"))
    if isinstance(raw_ans_data, dict) and "answers" in raw_ans_data and isinstance(raw_ans_data["answers"], dict):
        ans_map = raw_ans_data["answers"]
    else:
        ans_map = raw_ans_data

    meta = json.loads(meta_file.read_text(encoding="utf-8")) if meta_file.is_file() else {}
    q_meta = meta.get("questions", {})

    qids = list(key.keys())
    correct_flags: List[bool] = []
    chosen_hist: Counter = Counter()

    rec_k, rec_n = 0, 0
    nonrec_k, nonrec_n = 0, 0
    by_tag: Dict[str, List[int]] = defaultdict(lambda: [0, 0])
    by_scn: Dict[str, List[int]] = defaultdict(lambda: [0, 0])

    for qid in qids:
        gold = key[qid]
        pred = parse_choice_letter(ans_map.get(qid, ""))
        chosen_hist[pred] += 1
        is_ok = (pred == gold)
        correct_flags.append(is_ok)

        qm = q_meta.get(qid, {})
        tag = qm.get("tag", "UNKNOWN")
        scn = qm.get("scenario", "UNKNOWN")
        is_rec = bool(qm.get("is_recovery", is_recovery_tag(tag)))

        by_tag[tag][1] += 1
        by_scn[scn][1] += 1
        if is_ok:
            by_tag[tag][0] += 1
            by_scn[scn][0] += 1

        if is_rec:
            rec_n += 1
            if is_ok:
                rec_k += 1
        else:
            nonrec_n += 1
            if is_ok:
                nonrec_k += 1

    k = sum(1 for x in correct_flags if x)
    n = len(qids)
    lo, hi = wilson(k, n)
    micro_acc = (k / n) if n else 0.0

    scn_accs = [v[0] / v[1] for v in by_scn.values() if v[1] > 0]
    macro_acc = sum(scn_accs) / len(scn_accs) if scn_accs else micro_acc

    rec_lo, rec_hi = wilson(rec_k, rec_n)
    nonrec_lo, nonrec_hi = wilson(nonrec_k, nonrec_n)

    total_tokens = meta.get("total_prompt_bpe_tokens", 0)
    mean_tokens = meta.get("mean_prompt_bpe_tokens", 0.0)
    # Accuracy percentage points gained above 25% chance per 1,000 prompt tokens
    acc_gain_pct = (micro_acc - 0.25) * 100.0
    gain_per_1k_tok = round((acc_gain_pct / (total_tokens / 1000.0)), 2) if total_tokens > 0 else 0.0

    # Print backwards-compatible top summary line + detailed stratified report
    mode_banner = "[Protocol Header Mode: --keep-ctx]" if keep_ctx else "[Strict Blind Mode: @CTX & payloads stripped]"
    print(f"cond {cond} {mode_banner}: {k}/{n} = {micro_acc:.0%}  (95% CI {lo:.0%}-{hi:.0%}; chance 25%)")
    print(f"  - Micro Accuracy       : {k}/{n} ({micro_acc:.1%}) | Macro Accuracy (by scenario): {macro_acc:.1%}")
    if rec_n > 0 or nonrec_n > 0:
        rec_p = (rec_k / rec_n) if rec_n else 0.0
        nonrec_p = (nonrec_k / nonrec_n) if nonrec_n else 0.0
        print(
            f"  - Routine Recovery     : {rec_k}/{rec_n} ({rec_p:.1%}, 95% CI {rec_lo:.0%}-{rec_hi:.0%})"
        )
        print(
            f"  - Non-Recovery Domains : {nonrec_k}/{nonrec_n} ({nonrec_p:.1%}, 95% CI {nonrec_lo:.0%}-{nonrec_hi:.0%})"
        )
    if total_tokens > 0:
        print(
            f"  - Token Cost & Gain    : {total_tokens} total BPE tokens ({mean_tokens:.1f}/q) | "
            f"Gain over chance per 1k tokens: {gain_per_1k_tok:+.2f}%pt/1k tok"
        )

    hist_parts = []
    for L in list(LETTERS) + ["INVALID"]:
        cnt = chosen_hist.get(L, 0)
        if L != "INVALID" or cnt > 0:
            pct = (cnt / n) * 100.0 if n else 0.0
            bar = "#" * int(round(pct / 5.0))
            hist_parts.append(f"{L}:{cnt}({pct:.0f}%){bar}")
    print(f"  - Option Histogram     : {' | '.join(hist_parts)}")

    return {
        "condition": cond,
        "keep_ctx": keep_ctx,
        "rotate_options": rotate_options,
        "correct": k,
        "total": n,
        "micro_accuracy": round(micro_acc, 4),
        "macro_accuracy": round(macro_acc, 4),
        "wilson_95_ci": [round(lo, 4), round(hi, 4)],
        "recovery_subset": {
            "correct": rec_k,
            "total": rec_n,
            "accuracy": round(rec_k / rec_n, 4) if rec_n else 0.0,
            "wilson_95_ci": [round(rec_lo, 4), round(rec_hi, 4)],
        },
        "non_recovery_subset": {
            "correct": nonrec_k,
            "total": nonrec_n,
            "accuracy": round(nonrec_k / nonrec_n, 4) if nonrec_n else 0.0,
            "wilson_95_ci": [round(nonrec_lo, 4), round(nonrec_hi, 4)],
        },
        "by_domain_tag": {
            t: {"correct": v[0], "total": v[1], "accuracy": round(v[0] / v[1], 4) if v[1] else 0.0}
            for t, v in sorted(by_tag.items())
        },
        "option_histogram": {L: chosen_hist.get(L, 0) for L in list(LETTERS) + ["INVALID"]},
        "total_prompt_bpe_tokens": total_tokens,
        "mean_prompt_bpe_tokens": mean_tokens,
        "gain_over_chance_per_1k_tokens": gain_per_1k_tok,
        "correct_vector": correct_flags,
    }


def score(a: argparse.Namespace) -> Dict[str, Any]:
    out_dir = Path(a.out)
    res = evaluate_answers(
        out_dir,
        a.cond,
        Path(a.answers),
        keep_ctx=getattr(a, "keep_ctx", False),
        rotate_options=getattr(a, "rotate_options", False),
    )
    if getattr(a, "compare_answers", None) and getattr(a, "compare_cond", None):
        other = evaluate_answers(
            out_dir,
            a.compare_cond,
            Path(a.compare_answers),
            keep_ctx=getattr(a, "keep_ctx", False),
            rotate_options=getattr(a, "rotate_options", False),
        )
        mcn = mcnemar_test(res["correct_vector"], other["correct_vector"])
        print(
            f"  - McNemar ({a.cond} vs {a.compare_cond}): "
            f"b={mcn['b_only_first_correct']}, c={mcn['c_only_second_correct']}, "
            f"chi2_cc={mcn['chi2_cc']}, exact p={mcn['p_value_exact']} "
            f"({'SIGNIFICANT p<0.05' if mcn['significant_p05'] else 'ns'})"
        )
        res["mcnemar_vs_" + a.compare_cond] = mcn
    return res


def call_llm_backend(
    backend: str,
    model: str,
    prompt_text: str,
    timeout: int = 90,
) -> str:
    """
    Call the specified LLM backend with strict `temperature=0` and minimal `max_tokens`.
    Supported backends: `ollama`, `anthropic`, `openai`, `gemini`.
    """
    full_prompt = (
        "Pick the option that best matches the intent of the MESSAGE. "
        "Reply with one letter only (A, B, C, or D).\n\n" + prompt_text
    )

    if backend == "anthropic":
        req = urllib.request.Request(
            "https://api.anthropic.com/v1/messages",
            method="POST",
            headers={
                "content-type": "application/json",
                "anthropic-version": "2023-06-01",
                "x-api-key": os.environ["ANTHROPIC_API_KEY"],
            },
            data=json.dumps(
                {
                    "model": model,
                    "temperature": 0.0,
                    "max_tokens": 5,
                    "messages": [{"role": "user", "content": full_prompt}],
                }
            ).encode("utf-8"),
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))["content"][0]["text"].strip()

    if backend == "openai":
        base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
        req = urllib.request.Request(
            f"{base_url}/chat/completions",
            method="POST",
            headers={
                "content-type": "application/json",
                "authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
            },
            data=json.dumps(
                {
                    "model": model,
                    "temperature": 0.0,
                    "max_tokens": 5,
                    "messages": [{"role": "user", "content": full_prompt}],
                }
            ).encode("utf-8"),
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))["choices"][0]["message"]["content"].strip()

    if backend == "gemini":
        api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY", "")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        req = urllib.request.Request(
            url,
            method="POST",
            headers={"content-type": "application/json"},
            data=json.dumps(
                {
                    "contents": [{"parts": [{"text": full_prompt}]}],
                    "generationConfig": {"temperature": 0.0, "maxOutputTokens": 5},
                }
            ).encode("utf-8"),
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["candidates"][0]["content"]["parts"][0]["text"].strip()

    if backend == "ollama":
        host = os.environ.get("OLLAMA_HOST", "http://localhost:11434").strip()
        if not host.startswith("http"):
            host = f"http://{host}"
        url = f"{host.rstrip('/')}/api/generate"
        req = urllib.request.Request(
            url,
            method="POST",
            headers={"content-type": "application/json"},
            data=json.dumps(
                {
                    "model": model,
                    "prompt": full_prompt,
                    "stream": False,
                    "think": False,
                    "options": {"temperature": 0.0, "num_predict": 8},
                }
            ).encode("utf-8"),
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return str(data.get("response", "")).strip()

    raise ValueError(f"Unsupported backend: {backend}")


def run_single_condition(a: argparse.Namespace, cond: str) -> Dict[str, Any]:
    out_dir = Path(a.out)
    suf = file_suffix(
        cond,
        keep_ctx=getattr(a, "keep_ctx", False),
        rotate_options=getattr(a, "rotate_options", False),
    )
    q_path = out_dir / f"questions_{suf}.md"
    if not q_path.is_file():
        codec = ElegantCodec()
        items = load_items(codec)
        chosen = select_stratified_items(items, a.n, a.seed)
        build_for_condition(
            codec,
            items,
            chosen,
            cond,
            a.seed,
            out_dir,
            keep_ctx=getattr(a, "keep_ctx", False),
            rotate_options=getattr(a, "rotate_options", False),
        )

    qs = q_path.read_text(encoding="utf-8").strip().split("\n\n")
    backend = getattr(a, "backend", "anthropic")
    model = a.model or (
        "Gemma4-26B-PhenoX:latest" if backend == "ollama" else "claude-3-5-sonnet-20241022"
    )
    safe_model = re.sub(r"[^A-Za-z0-9_.-]+", "_", model)

    ans: Dict[str, str] = {}
    raw_outputs: Dict[str, str] = {}
    for q in qs:
        qid = q.split("\n", 1)[0].strip()
        try:
            raw_txt = call_llm_backend(backend, model, q)
        except Exception as exc:
            raw_txt = f"ERROR: {exc}"
        raw_outputs[qid] = raw_txt
        ans[qid] = parse_choice_letter(raw_txt)

    ans_file = out_dir / f"answers_{suf}_{safe_model}.json"
    payload = {
        "model": model,
        "backend": backend,
        "temperature": 0.0,
        "condition": cond,
        "keep_ctx": bool(getattr(a, "keep_ctx", False)),
        "rotate_options": bool(getattr(a, "rotate_options", False)),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "answers": ans,
        "raw_responses": raw_outputs,
    }
    ans_file.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    eval_res = evaluate_answers(
        out_dir,
        cond,
        ans_file,
        keep_ctx=getattr(a, "keep_ctx", False),
        rotate_options=getattr(a, "rotate_options", False),
    )
    payload["evaluation"] = {k: v for k, v in eval_res.items() if k != "correct_vector"}
    ans_file.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return eval_res


def run(a: argparse.Namespace) -> None:
    conds = list(VALID_CONDS) if a.cond == "ALL" else [a.cond]
    results_by_cond: Dict[str, Dict[str, Any]] = {}
    for c in conds:
        results_by_cond[c] = run_single_condition(a, c)

    if len(results_by_cond) >= 2:
        print("\n=== Paired McNemar Tests ===")
        pairs = [("A", "B"), ("B", "C"), ("B", "D"), ("A", "E"), ("B", "E")]
        for c1, c2 in pairs:
            if c1 in results_by_cond and c2 in results_by_cond:
                mcn = mcnemar_test(
                    results_by_cond[c1]["correct_vector"],
                    results_by_cond[c2]["correct_vector"],
                )
                print(
                    f"  {c1} vs {c2}: b={mcn['b_only_first_correct']}, c={mcn['c_only_second_correct']}, "
                    f"chi2_cc={mcn['chi2_cc']}, exact p={mcn['p_value_exact']} "
                    f"({'SIGNIFICANT p<0.05' if mcn['significant_p05'] else 'ns'})"
                )


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="TOAI-elegant-lang v5.4.3 Receiver-Comprehension Evaluation Harness"
    )
    ap.add_argument("mode", choices=["build", "score", "run"])
    ap.add_argument("--cond", choices=list(VALID_CONDS) + ["ALL"], required=True)
    ap.add_argument("-n", type=int, default=24)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--out", default="/tmp/qa")
    ap.add_argument("--answers", help="Path to answers JSON file (for score mode)")
    ap.add_argument("--compare-cond", choices=list(VALID_CONDS), help="Second condition for paired McNemar test")
    ap.add_argument("--compare-answers", help="Second answers JSON file for paired McNemar test")
    ap.add_argument("--model", default="Gemma4-26B-PhenoX:latest")
    ap.add_argument(
        "--backend",
        choices=["ollama", "anthropic", "openai", "gemini"],
        default="anthropic",
        help="LLM backend for run mode (all enforce temperature=0)",
    )
    ap.add_argument(
        "--keep-ctx",
        action="store_true",
        help="Protocol Header Mode: keep @CTX and masked [key:*] structure (isolated from blind A-E)",
    )
    ap.add_argument(
        "--rotate-options",
        action="store_true",
        help="Emit/score all 4 cyclic option rotations (A/B/C/D) per question to eliminate position bias",
    )
    args = ap.parse_args()
    {"build": build, "score": score, "run": run}[args.mode](args)
