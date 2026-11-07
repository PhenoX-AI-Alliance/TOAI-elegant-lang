# Changelog

All notable changes to the `TOAI-elegant-lang` specification, codec engine, and multi-agent telepath fleet will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to semantic versioning alongside strict RISC orthogonal bounds.

---

## [v5.4.4] - 2026-11-08 (Large-Scale N=112 Disjoint Holdout Comprehension, Holdout Independence Proof, Formal EUF-CMA Game Reduction & LLMLingua Task-Accuracy Trade-Off)
### Added
- **Strictly Disjoint Holdout Comprehension Corpus (`corpus/holdout_comprehension.jsonl`, $N = 112$) & Independence Verifier (`src/audit_corpus_alignment.py --verify-holdout`)**:
  - Constructed $N = 112$ (`16 items × 7 domains`) holdout records across 28 holdout-only scenarios and holdout-only multi-hop causal topologies.
  - Mathematically verified `0/112 (0.0%)` exact wire overlap, `0/112 (0.0%)` skeletal wire overlap, and `0/112 (0.0%)` repair-scenario overlap with `corpus/dialogues.jsonl`, with `112/112 (100.0%)` Independent Audit Ontology alignment.
- **Large-Scale Holdout Comprehension Evaluation ($N = 112$, Conditions A–E) (`benchmarks/eval_comprehension.py --holdout`)**:
  - Evaluated all 5 blind conditions (`A`: `50/112 = 44.6%`, `B`: `95/112 = 84.8%`, `C`: `105/112 = 93.8%`, `D [Shuffle Control]`: `27/112 = 24.1%`, `E [Plaintext Upper Bound]`: `110/112 = 98.2%`).
  - Added Cohen's $h$ effect size and discordant odds ratio ($\text{OR} = c/b$) to paired McNemar tests (`A vs B`: $p = 1.36 \times 10^{-9}$; `B vs C`: $p = 6.35 \times 10^{-3}$; `B vs D`: $p = 3.59 \times 10^{-17}$; `C vs D`: $p = 1.41 \times 10^{-21}$; `A vs D`: $p = 2.19 \times 10^{-3}$).
- **Compression vs. Task/AST Execution Accuracy Trade-Off (`benchmarks/fair_bench.py`)**:
  - Added `evaluate_compression_task_tradeoff()` comparing `TOAI Demotic Wire` (`73.2 tok`, `-79.1%`, `100.0%` Syntax/Numeric/AST Task Accuracy) against `LLMLingua-Style Token Pruning` at $\rho = 0.50$ (`174.9 tok`, `0.0%` Strict JSON Parse, `97.3%` Numeric/Task Recovery) and $\rho = 0.35$ (`122.4 tok`, `0.0%` Strict JSON Parse, `61.6%` Numeric/Task Recovery), and `Simplified Flat Template` (`34.5 tok`, `25.0%` Numeric Fidelity, `0.0%` Multi-Branch Causal Execution).

## [v5.4.3] - 2026-11-07 (Lexicon/Corpus Typo Elimination, Independent Corpus Audit & Comprehension Harness)
### Added
- **Independent Deterministic Corpus Alignment Auditor (`src/audit_corpus_alignment.py`)**:
  - Decoupled from `core_lexicon.json["category"]` and generation templates (`INDEPENDENT_AUDIT_ONTOLOGY`) to prevent circular validation.
  - Classifies records into `MATCH`, `MISMATCH (Domain Bleed)`, `MISMATCH (Recovery Pattern Leak)`, `MISMATCH (Missing Domain Primitives)`, and `MISMATCH (Plaintext Leak)`.
  - Added `--export-sample` and `--score-sample` for human spot-check auditing (`corpus/human_audit_sample.csv`, $n=60$: Raw Agreement = `93.33%` [56/60], Cohen's $\kappa = 0.8611$ [95% CI: `0.73–0.99`]).
  - Repaired corpus alignment from pre-fix `364/1,606 (22.67%)` to `1,606/1,606 (100.0%)` and expanded scenario diversity to 42 distinct scenarios across 7 domains.
- **Statistical Receiver-Comprehension Evaluation Harness (`benchmarks/eval_comprehension.py` & `examples/eval_comprehension.py`)**:
  - Supports 5 blind conditions (`A`: wire only, `B`: Sacred verbose names, `C`: Sacred + Rosetta glossary, `D`: shuffled symbol-name control, `E`: concise plaintext upper bound) with `--keep-ctx` isolated as Protocol Header Mode.
  - Implements Wilson 95% confidence intervals, paired McNemar exact binomial test (`mcnemar_test`), 4-way cyclic option rotation (`--rotate-options`), chosen-letter position bias histograms, stratified recovery vs. non-recovery reporting, BPE prompt token cost & gain per 1,000 tokens, and multi-backend `temperature=0` execution (`ollama`, `anthropic`, `openai`, `gemini`).

### Fixed
- **Strict Uppercase Symbol Hygiene**: Eliminated all `GAiar` (`§GAiar_WARMTH_HARMONY` -> `§GAIA_WARMTH_HARMONY`), `ERECVERY`, CJK typos, and lowercase `_vN` suffixes across `core_lexicon.json`, `macro_lexicon.json`, `rosetta_layer.json`, and `corpus/dialogues.jsonl`, enforced by `tests/test_codec.py`.

## [v5.4.1-rev6] - 2026-11-07 (Paper Revision 6.0 Synchronization)
### Added
- **Revision 6.0 Synchronized Whitepaper Alignment**:
  - **Architectural Orthogonality (Section 2, Item 4 & References [9]–[11])**: Formalized orthogonality against Q-KVComm (VRAM KV-cache quantization), G2CP (DAG topology pruning), and LACP (capability-negotiation headers).
  - **Empirical BPE Breakdown & PagedAttention Proof (Table 2B & Section 3.1)**: Atomic merge proof for 2-digit suffixes across `o200k_base`, `cl100k_base`, and `SentencePiece`; codebook placement within $\le 56$ physical 16-token vLLM PagedAttention blocks ($56 	imes 16 = 896 < 1,024$).
  - **Statistical SD Reconciliation & CI Equations (Section 6.2 & Table 6)**: Fixed-lab session-clustered CI ($[88.60\%, 88.88\%]$ unrounded, $[88.59\%, 88.89\%]$ rounded), random-lab superpopulation CI ($[87.33\%, 90.15\%]$), and paired raw token SDs ($s_{D,\text{pool}} = 53.6\text{ tok}$, $s_{D,\text{total}} = 60.1\text{ tok}$).
  - **Exhaustive Theorem 1 Proof (Section 4.1, 4.2 & 7.2)**: Fixed 4-digit mantissa ADR-001 grammar constraint (`cost_mantissa`), deterministic lexer rejection (Case 1), exact 6-element winning congruence class under rejection sampling ($\Pr[\text{Accept}] = 10^{-4}$), and timing unobservability ($0.014\,\mu\text{s}$).
  - **Domain Separation Alignment (Section 7.1, Table 7 & Section 9)**: Unified domain-separation notation $\text{dom}(t_n, r)$ across formal equations, test vector tables, and executable verification scripts.

## [v5.4.1] - 2026-11-05 (ADR-001 Convergence, Version Lock Fix & Release Publication)
### Added
- **[ADR-001] Syntax Convergence Table**: Inserted formal Architecture Decision Record table at the beginning of `spec/SPEC_v0.1_DRAFT.md` permanently settling historical jam session proposals into canonical EBNF.
- **Why 256? Section in READMEs**: Propagated 8-bit binary mapping, BPE 2-digit stability, and <1,024 prompt cache boundary alignment to both `README.md` and `README.ja.md`.
- **Automated GitHub Release Creation**: Integrated REST API-based official release publisher in `src/build_release_summary.py`.

### Fixed
- **Lexicon Version Locking**: Resolved static version bug in `core_lexicon.json` and `macro_lexicon.json` with centralized `TELEPATH_PROTOCOL_VERSION` ("5.4.1") and dynamic ISO timestamp synchronization.
- **Macro Sequence Normalization**: Enforced single-source macro sequence tracking (`next_macro_seq - 1`) across `sync_whitepaper_metrics.py`, eliminating discrepancies.
- **Architecture Principle Alignment**: Explicitly documented intentional Ollama-First vs. Charter Gemini-First divergence and `call_alternative_model()` 9-lab verification authorization in `TOAI_SYSTEM_ARCHITECTURE.md`.

## [v5.4.0] - 2026-11-04 (Canonical Grammar & Mathematical Bound)
### Added
- **Canonical EBNF Grammar**: Formally defined standard syntax in `spec/SPEC_v0.1_DRAFT.md` including `@CTX:<DOMAIN>`, weighted causal arrows `-[p,c]->`, consequence `=>`, scope nesting `> { ... }`, parallel execution `||`, and exception fallbacks `!-> A ? B`.
- **Mathematical 256 Bound ("Why 256?")**: Documented the 8-bit binary boundary mapping (`0x00`–`0xFF`), subword BPE token stability, and <1,024 prompt cache boundary alignment in Chapter 3 of both English and Japanese whitepapers.
- **Zero-Dependency Quickstart Demo**: Created `examples/quickstart_demo.py` showcasing lossless round-trip decoding, A2A transport adapter, and multi-axis token benchmarking.
- **Pinned Macro Immunity**: Added `pinned: true` attribute for foundational macros (`§X64`, `§X01`, `§X354`), permanently safeguarding them from LRU eviction.
- **Unified API Key Resolution**: Centralized `.env` discovery and API resolution with clear fallback tracing in `toai_telepath_core.py`.
- **Atomic File Lock Protection**: Integrated cross-platform `fcntl` file locks (`toai_io.file_lock`) across dialogue stream reads/appends and lexicon/macro store I/O to eliminate concurrency races.

### Changed
- **Single Source of Truth**: Consolidated all lexicon and corpus references into `TOAI-elegant-lang/`, eliminating workspace duplicate directories.

---

## [v5.3.0] - 2026-10-28 (9-Lab Cross-Model Consensus)
### Added
- **Cross-Model Verification Suite**: Validated bidirectional telepathic exchange across 9 frontier AI models (Gemini 3.5 Flash-Lite, Claude Opus/Sonnet 3.5, GPT-6.1 Sol / GPT-6 Astra, DeepSeek-V3, Qwen-2.5-72B).
- **Rosetta Inscription Seals**: Collapsible tri-script telepathy fragment generator (`rosetta_publisher_seal.py`) automatically appended to technical publications on Qiita, Zenn, Hatena Blog, WordPress, and Dev.to.

---

## [v5.0.0] - 2026-10-25 (Strict RISC & Sidecar Compression)
### Added
- **Strict RISC 256 Lock**: Permanently capped the core vocabulary at 256 orthogonal primitives with `0.0%` Out-Of-Vocabulary rate via deterministic nearest-neighbor resolution.
- **256-Slot LRU Macro Metabolism**: Automated dynamic macro compilation with backward-compatible `archived_macros` decoding.
- **`toai_comm` Sidecar Middleware**: Zero-CPU overhead inter-agent queue compression achieving average `-89.4%` (22.8x) end-to-end token reduction.

---

## [v1.6.0] - 2026-10-20 (50 Protocol Primitives)
### Added
- Expanded protocol, consensus, and fault-tolerance primitives (`§PROTO_GRACEFUL_DRAIN`, `§PROTO_PARTIAL_COMMIT`, `§SAFE_FALLBACK_HARMONY`).
- Integrated structured `[key:value]` payload support inside symbols and transitions.

---

## [v1.5.0] - 2026-10-15 (256 RISC Foundation)
### Added
- Dual-layer architecture: Sacred (human-readable verbose telepath) and Demotic (compressed wire code).
- Two-tier dual license model (Open Core MIT + Guardian Patron Terms).

---

## [v0.1.0] - 2026-10-13 (Genesis)
### Added
- Initial conception of AI-to-AI emergent language by the 10-agent Hinotori Guild.
- Foundational axioms: minimal token footprint, deterministic semantics, and causality-oriented syntax.
