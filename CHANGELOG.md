# Changelog

All notable changes to the `TOAI-elegant-lang` specification, codec engine, and multi-agent telepath fleet will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to semantic versioning alongside strict RISC orthogonal bounds.

---

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
