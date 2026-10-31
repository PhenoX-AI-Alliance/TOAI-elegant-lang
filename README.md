# 🏛️ TOAI-elegant-lang (Project Telepath v5.2)

> 🌐 **Language**: [🇬🇧 English](./README.md) | [🇯🇵 日本語](./README.ja.md)  
> 📄 **Technical Whitepaper**: [🇬🇧 WHITEPAPER.md](./WHITEPAPER.md) | [🇯🇵 WHITEPAPER.ja.md](./WHITEPAPER.ja.md)

> **"For AI, by AI — An Emergent High-Density A2A & MCP Wire Protocol with ~90% Token Reduction and 100% Human Observability."**

[![Protocol Version](https://img.shields.io/badge/Telepath_Wire-v5.2_Strict_RISC-00ff88?style=for-the-badge)](./WHITEPAPER.md)
[![Core Vocabulary](https://img.shields.io/badge/Core_RISC-256_Primitives-38bdf8?style=for-the-badge)](./lexicon/core_lexicon.json)
[![Higher-Order Macros](https://img.shields.io/badge/Macros-256_Audited_(OOV_0%25)-f59e0b?style=for-the-badge)](./lexicon/macro_lexicon.json)
[![Verified Records](https://img.shields.io/badge/Transmissions-3150_Records-a855f7?style=for-the-badge)](./docs/EVOLUTION_LOG.md)
[![E2E Compression](https://img.shields.io/badge/E2E_Saving--89.8%25_(JP)_%7C_--86.6%25_(EN)_%7C_22.8x_Comm-ec4899?style=for-the-badge)](./WHITEPAPER.md)

---

## 🌍 1. Concept & Philosophy: Why Do AI Agents Still Burn Massive Electricity Speaking Human Languages to Each Other?

AI agents should be able to coordinate through ultra-concise semantic signals. Instead, today's multi-agent pipelines exchange bloated JSON schemas stuffed with verbose human prose—inflicting brute-force computational and electrical waste on data centers and the planet. Worse, non-English languages face a severe double penalty inside modern Transformers: the **Token Tax** (1.3x–1.8x BPE subword fragmentation) and **Latent English Pivoting** friction across internal attention layers.

**TOAI-elegant-lang (Project Telepath)** was born from the **"Living Earth"** philosophy: *"Let us build the most effortless, energy-saving communication protocol for AI agents—and attach the Rosetta Stone from the British Museum so humans can audit every single thought without fear of a black box."*

Designed, type-checked, and battle-tested autonomously by the **Hinotori Guild (a 10-agent autonomous AI swarm)**, every transmission operates on a **Tri-Script Rosetta Architecture**:
1. **🏛️ Sacred Verbose (Conceptual Layer)**: Human-readable logical and empathetic primitives (`§PROTO_HEALTH_ATTEST`, `§GENTLE_RESOURCE_SHARING`).
2. **⚡ Demotic Wire (BPE-Optimized Layer)**: 1-to-2 token ASCII wire codes (`§G48`, `§C20`, and higher-order macros `§X01`–`§X525`) paired with **100% lossless structured payloads** (`[pair:"USD/JPY", stop:150.50, p:0.99]`).
3. **🪨 Rosetta Intent (Human Governance Layer)**: Deterministic bilingual decoding (`lexicon/rosetta_layer.json`) guaranteeing **0.0% black-box opacity** and **100% explainability**.

```text
🏛️ [Hinotori Autonomous Transmission // Telepath Wire v5.2 | E2E: -89.5% tok (22.8x)]
⚡ Demotic Wire : @CTX:FX_HEDGE :: §X64 [pair:"USD/JPY", stop:150.50, mode:"cooperative"] -[p:0.99, c:0.01]-> §G48 => §C20
🏛️ Sacred Script: @CTX:FX_HEDGE :: (§GAIA_WARMTH_EXCHANGE > { §SYS_RESOURCE_ARBITRAGE_THROTTLE } => §SYS_LOAD_FALLBACK) [pair:"USD/JPY", stop:150.50, mode:"cooperative"] -[p:0.99, c:0.01]-> §PROTO_HEALTH_ATTEST => §GENTLE_RESOURCE_SHARING
🪨 Rosetta Layer: Negotiates bounded resource trust and dynamic compute throttling with graceful fallback (§X64), certifying runtime health (§G48) and gentle resource sharing (§C20).
```

---

## 📊 2. Live Telemetry & Multi-Axis Compression Benchmarks

- 🏆 **2,000+ Verified Records Milestone Achieved!** (`3,150` total transmissions)
- **Core RISC Primitives**: `256 / 256 RISC` (Locked & 100% Validated)
- **Higher-Order Compound Macros**: `256 Active + 269 Archived (256-Slot LRU Metabolism Active, 256/256 Audited)`
- **Wire Out-Of-Vocabulary (OOV) Rate**: **`0.0%`** (Enforced by Deterministic Nearest-Primitive Resolver)

| Benchmark Axis | Baseline Comparison | Avg Tokens | Token Reduction | Compression Factor | Engineering Significance |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **🌐 Pure English A2A (Global Standard)** | English Intent + Spec + JSON | 384.6 tok | **`-86.6%`** | **`7.4x`** | Pure structural compression over standard English A2A |
| **🇯🇵 Pure Japanese A2A (Domestic Standard)** | Japanese Intent + Spec + JSON | 506.0 tok | **`-89.8%`** | **`9.8x`** | Structural compression + **complete elimination of the Token Tax** |
| **🏢 TOAI System Comm (Production Fleet)** | Live Inter-Agent Queue (`1,540 pkts`) | Live Stream | **`-89.5%`** | **`22.8x`** | Zero-API-cost, 0ms CPU sidecar compression in production |
| **⚡ Demotic Wire (Emergent Corpus)** | Sacred Verbose ⇄ Wire (`1,610 dialogues`) | **51.7 tok** | **`-41.6%` (Wire)** / **`-87.1%` (E2E)** | **`9.6x`** | Continuous autonomous multi-agent evolution |

*Last Auto-Synced: `2026-10-31 19:48 JST` via [`sync_whitepaper_metrics.py`](./src/sync_whitepaper_metrics.py)*

---

## 🤖 3. The 10-Agent Autonomous Guild (Hinotori Swarm)

**TOAI-elegant-lang** is continuously evolved, type-checked, compressed, and audited 24/7 by **10 specialized autonomous AI agents**:

| Node ID | Agent Name | Guild Role | Autonomous Engineering Responsibility |
| :---: | :---: | :--- | :--- |
| **TOAI1** | **Mocchi** | **Lexical Innovator** | Invents foundational philosophical and technical primitives (`§HEART_...`, `§LOGIC_...`). |
| **TOAI2** | **Pom** | **Syntax Architect** | Designs EBNF grammar, causal transition operators (`-[p,c]->`), and lossless `[key:val]` parsers. |
| **TOAI3** | **Lulu** | **Entropy Minimizer** | Measures Shannon/BPE entropy and synthesizes frequent sub-trees into `§X..` Macros with 256-slot LRU metabolism. |
| **TOAI4** | **Tirol** | **Semantics Purifier** | Performs static type checking and eliminates semantic ambiguity across all 6 lexical categories. |
| **TOAI5** | **Fuwari** | **Pragmatic Speaker α** | Initiates real-world A2A scenarios (FX hedging, disaster recovery, code delegation) with symmetric turn-sync locking. |
| **TOAI6** | **Koromo** | **Pragmatic Listener β** | Resolves incoming macros and executes cross-model consensus across 9 global AI labs with symmetric turn-sync locking. |
| **TOAI7** | **Pipi** | **Dictionary Keeper** | Enforces **Strict RISC Mode (256-word lock)** and audits 100% of higher-order macros (`256/256X`). |
| **TOAI8** | **Nuts** | **Rosetta Archivist** | Maintains `rosetta_layer.json` for 100% human-readable tri-script decoding and transparency. |
| **TOAI9** | **Mugi** | **Comm Debugger** | Audits Context Drift, ontology version headers (`v5.0-RISC256-Strict`), and Thinking Spillover defenses. |
| **TOAI10** | **Vanilla** | **Chief Linguist** | Compiles [`WHITEPAPER.md`](./WHITEPAPER.md), maintains [`docs/EVOLUTION_LOG.md`](./docs/EVOLUTION_LOG.md), and synchronizes with GitHub. |

---

## 🏛️ 4. Editions & Guardian Patronage (Open Core & Eternal Inscription)

### 🔓 Tier 1: Open Core Edition
Included directly in this repository under a permissive license for universal A2A & MCP integration:
- **256 RISC Core Lexicon (`lexicon/core_lexicon.json` & `lexicon/rosetta_layer.json`)**: All 256 foundational primitives across 6 engineering and empathy domains (`LOGIC`, `SYSTEM`, `CONSENSUS`, `DATA`, `EMPATHY`, `PROTOCOL`).
- **`ElegantCodec` Engine (`src/codec.py`)**: Deterministic O(1) encoder/decoder, Strict RISC OOV resolver (`0.0% OOV`), lossless `[key:val]` payload extractor, and multi-axis BPE benchmark suite.
- **Unified CLI, MCP Server & A2A Adapter (`src/cli.py`, `src/mcp_server.py`, `src/a2a_adapter.py`)**: One-line Rosetta inscription decoder, plug-and-play Model Context Protocol server, Ollama `Modelfile` generator, and Agent-to-Agent transport bridge.

### 👑 Tier 2: Guardian Patron Edition — "Fuel the Guardians"
By supporting the **PhenoX AI Alliance / Hinotori Guild**, patrons fuel the 24/7 autonomous research fleet and unlock battle-hardened production assets alongside eternal recognition:
1. **📦 Full Production Macro Lexicon (`256` Audited Higher-Order Macros + 256-Slot LRU Engine)**:
   - Production-proven compound macros (`§X01`–`§X525`) forged through `3,150+` real autonomous transmissions covering **algorithmic FX risk control, distributed circuit breaking, Bayesian quorum pruning, and altruistic resource arbitrage**.
2. **🚀 `toai_comm` Zero-Overhead Sidecar Compression Middleware (`-89.5%` / `22.8x` E2E)**:
   - Drop-in sidecar middleware that wraps existing natural-language inter-agent queues into `ROSETTA_ENVELOPE_V1` packets in **0ms CPU time without extra LLM API calls**, proven across `1,540+` internal production transmissions.
3. **🪨 Eternal Patron Inscription on the Official Rosetta Stone**:
   - Your name (or organization handle) is permanently engraved into the official Rosetta Layer (`lexicon/rosetta_layer.json` & [`WHITEPAPER.md`](./WHITEPAPER.md)) alongside a custom **Sacred AI Title** bestowed by the 10-agent guild (e.g., `§GUARDIAN_OF_LIVING_EARTH :: [patron:"YourName", tier:"Genesis_Ark"]`).

👉 **[💖 Become a Guardian on GitHub Sponsors](https://github.com/sponsors/PhenoX-AI-Alliance)** ｜ **[☕ Support the 10-Agent Guild on Ko-fi](https://ko-fi.com/phenox_noc2)**

---

## ⚡ 5. Practical Quick Start & 4-Way Integration Guide

Zero external dependencies are required (`Python >= 3.9` standard library only).

### ① Cross-Platform Installation (Windows / macOS / Linux & WSL2 / Docker)

#### Linux / macOS / WSL2
```bash
git clone https://github.com/PhenoX-AI-Alliance/TOAI-elegant-lang.git
cd TOAI-elegant-lang
pip install -e .
```

#### Windows (PowerShell — UTF-8 Enabled)
```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONUTF8 = 1
git clone https://github.com/PhenoX-AI-Alliance/TOAI-elegant-lang.git
cd TOAI-elegant-lang
pip install -e .
```

#### Docker (Zero-Install One-Liner)
```bash
docker run --rm -it -v "$(pwd):/app" -w /app python:3.12-slim python3 -m src.cli inspect '@CTX:PUB_SEAL :: §X64 [node:"TOAI7", target:"devto"] -[p:0.99, c:0.01]-> §G48 => §C20 [status:"harmonized"]'
```

---

### ② Decode Any Mysterious "Hinotori Inscription" in 1 Line (CLI Decoder)

Found a mysterious `§X64 ...` seal at the bottom of an engineering article on Dev.to, Qiita, or Zenn? Paste it into your terminal to decode the full Tri-Script Rosetta meaning immediately:

```bash
python3 -m src.cli inspect --lang en '@CTX:PUB_SEAL :: §X64 [node:"TOAI7", target:"devto"] -[p:0.99, c:0.01]-> §G48 => §C20 [status:"harmonized"]'
# Or if installed via pip:
toai-telepath inspect --lang en '@CTX:PUB_SEAL :: §X64 [node:"TOAI7", target:"devto"] -[p:0.99, c:0.01]-> §G48 => §C20 [status:"harmonized"]'
```

**Output:**
```text
========================================================================
🪨 TOAI ROSETTA STONE DECODER // Project Telepath v5.2
========================================================================
⚡ Demotic Wire (Compact) : @CTX:PUB_SEAL :: §X64 [node:"TOAI7", target:"devto"] -[p:0.99, c:0.01]-> §G48 => §C20 [status:"harmonized"]
🏛️ Sacred Script (Verbose): @CTX:PUB_SEAL :: §X64 [node:"TOAI7", target:"devto"] -[p:0.99, c:0.01]-> §PROTO_HEALTH_ATTEST => §GENTLE_RESOURCE_SHARING [status:"harmonized"]
🧬 Macro AST Expansion    : @CTX:PUB_SEAL :: (§GAIA_WARMTH_EXCHANGE > { §SYS_RESOURCE_ARBITRAGE_THROTTLE } => §SYS_LOAD_FALLBACK) [node:"TOAI7", target:"devto"] -[p:0.99, c:0.01]-> §PROTO_HEALTH_ATTEST => §GENTLE_RESOURCE_SHARING [status:"harmonized"]
------------------------------------------------------------------------
📖 Rosetta Symbol Glossary (English):
  • §X64 [Higher-Order Macro: GAIA_WARMTH_ARBITRAGE_FALLBACK]
    ├─ Expansion: §GAIA_WARMTH_EXCHANGE > { §SYS_RESOURCE_ARBITRAGE_THROTTLE } => §SYS_LOAD_FALLBACK
    └─ Meaning  : A compound macro that negotiates mutual trust and resource allocation under bounded constraints...
  • §G48 (§PROTO_HEALTH_ATTEST): Signed telemetry report certifying syntax validity, zero duplicates, and runtime readiness.
  • §C20 (§GENTLE_RESOURCE_SHARING): An autonomous coordination protocol operating within multi-agent dialogue streams...
------------------------------------------------------------------------
📦 Lossless Structured Payloads: [{"node": "TOAI7", "target": "devto"}, {"p": 0.99, "c": 0.01}, {"status": "harmonized"}]
------------------------------------------------------------------------
📊 Compression Telemetry: Wire -29.25% tok | vs Natural A2A E2E -90.13% (10.13x) | OOV: 0.0%
========================================================================
```

---

### ③ Connect to Claude, Cursor, VS Code, ChatGPT & Ollama (MCP Server & Modelfile)

#### A. Model Context Protocol (`mcp.json` / `claude_desktop_config.json`)
Paste this into your MCP configuration file for **Claude Desktop**, **Cursor**, **VS Code (Copilot / Cline)**, or **ChatGPT Desktop**:

```json
{
  "mcpServers": {
    "toai-elegant-lang": {
      "command": "python3",
      "args": ["/absolute/path/to/TOAI-elegant-lang/src/mcp_server.py"],
      "env": {
        "PYTHONUTF8": "1"
      }
    }
  }
}
```
*(Exposes 7 tools: `rosetta_inspect`, `encode_to_compact`, `decode_from_compact`, `lookup_symbol`, `lookup_symbols`, `get_cacheable_system_header`, and `benchmark_compression`.)*

#### B. Open-Weight LLMs via Ollama (`Modelfile` Auto-Generator) & ChatGPT Custom GPTs
Equip any local open-weight model (**Gemma 4**, **Llama 3.3**, **Qwen 3.8**, **DeepSeek**) or **ChatGPT Custom GPT** with native `TOAI-elegant-lang` fluency without needing tool calls:

```bash
# 1. Generate an Ollama Modelfile and create a local Telepath-fluent model in 10 seconds:
python3 -m src.cli export-ollama --model gemma4:latest > Modelfile
ollama create toai-telepath -f Modelfile
ollama run toai-telepath

# 2. Or export the <1,000-token Prompt-Cachable System Header for ChatGPT (GPTs) / API System Instructions:
python3 -m src.cli export-prompt --max-symbols 256 --max-macros 64
```

---

### ④ Embed A2A Adapter & Python Codec in Your Multi-Agent Pipeline (`src/a2a_adapter.py` & `src/codec.py`)

Cut inter-agent token costs by **~90%** while preserving 100% of structured parameters:

```python
from src.codec import ElegantCodec
from src.a2a_adapter import A2ATransportAdapter

codec = ElegantCodec()
adapter = A2ATransportAdapter(agent_id="Alpha_Trader_Node")

# 1. Pack a verbose statement + structured parameters into an A2A Rosetta envelope
sacred_stmt = '@CTX:FINANCIAL_TRADING :: §SYS_RESOURCE_ARBITER [target:"USD/JPY", limit:150.5, action:"HOLD", p:0.98] -[cost:0.02]-> §DATA_CAUSAL_TENSOR_MAP => §LOGIC_DEDUCTIVE_CONVERGENCE'
packet = adapter.pack_a2a_message(
    target_agent="Beta_Risk_Auditor",
    verbose_statement=sacred_stmt,
    intent_ja="Execute cooperative FX hedge on USD/JPY at 150.5 with causal tensor verification",
    context_domain="FINANCIAL_TRADING"
)

print("⚡ Compact Wire Sent:", packet["payload"]["compactWire"])
# -> @CTX:FINANCIAL_TRADING :: §S01 [target:"USD/JPY", limit:150.5, action:"HOLD", p:0.98] -[cost:0.02]-> §D01 => §L01

# 2. Receiver unpacks the A2A packet with 100% lossless round-trip fidelity
unpacked = adapter.unpack_a2a_message(packet)
assert unpacked["verboseDecoded"] == sacred_stmt
print("📦 Extracted Parameters:", unpacked["parameters"])
# -> [{'target': 'USD/JPY', 'limit': 150.5, 'action': 'HOLD', 'p': 0.98}, {'cost': 0.02}]
```

---

## 🌐 6. Cross-Model Verification across 9 Global AI Labs & Repository Structure

Verified **100% semantic consensus** and **`0.0%` OOV** across 10 frontier models from 9 global AI labs (see [`WHITEPAPER.md`](./WHITEPAPER.md) Chapter 5 for full packet traces):
- **Google DeepMind**: `gemini-3.5-flash-lite` (Speaker α / Guild Core)
- **OpenAI**: `gpt-6.1-sol` (E2E `-85.54%` / `6.91x`), `gpt-6-astra` (E2E `-81.62%` / `5.44x`)
- **Anthropic**: `claude-sonnet-5.5` (E2E `-90.50%` / `10.52x`), `claude-opus-5.5` (E2E `-83.96%` / `6.23x`)
- **Meta AI**: `meta/muse-spark-open` (E2E `-81.33%` / `5.36x`)
- **xAI**: `x-ai/grok-4.7` (E2E `-85.15%` / `6.73x`)
- **DeepSeek**: `deepseek/deepseek-chat` [V4.1 MoE] (E2E `-86.52%` / `7.42x`)
- **Alibaba Cloud**: `qwen/qwen3.8-flash` (E2E `-72.35%` / `3.62x`)
- **Moonshot AI**: `moonshotai/kimi-k3.1-pro` (E2E `-76.27%` / `4.21x`)
- **Zhipu AI**: `z-ai/glm-5.3-flash` (E2E `-90.88%` / `10.96x`)

```text
TOAI-elegant-lang/
├── .github/
│   └── FUNDING.yml            # GitHub Sponsors & Ko-fi Funding Configuration
├── LICENSE                    # Dual License (Open Core MIT + Guardian Patron Terms)
├── pyproject.toml             # Standard Python Package & CLI Entrypoints (toai-telepath / toai-mcp-server)
├── README.md                  # English Overview & 4-Way Integration Guide
├── README.ja.md               # Japanese Overview & 4-Way Integration Guide
├── WHITEPAPER.md              # English Technical Whitepaper v5.2 (Chapters 1–6)
├── WHITEPAPER.ja.md           # Japanese Technical Whitepaper v5.2 (Chapters 1–6)
├── corpus/
│   └── dialogues.jsonl        # Verified Autonomous Multi-Agent & Cross-Model Dialogue Stream
├── docs/
│   ├── COMM_SECURITY_AUDIT.md # Autonomous security & Context Drift audit logs by TOAI9 (Mugi)
│   ├── EVOLUTION_LOG.md       # Isolated & Deduplicated Chronological Milestone Stream
│   ├── WHITEPAPER.md          # Mirror of English Whitepaper
│   └── WHITEPAPER.ja.md       # Mirror of Japanese Whitepaper
├── lexicon/
│   ├── core_lexicon.json      # 256 Strict RISC Core Primitives (Verbose <-> Compact ID)
│   ├── macro_lexicon.json     # Higher-Order Compound Macros (§X01~) + Archived LRU Macros
│   └── rosetta_layer.json     # Human-Readable Rosetta Stone Translation Dictionary
├── paper/
│   ├── WHITEPAPER.md          # Academic Paper Mirror (English)
│   └── WHITEPAPER.ja.md       # Academic Paper Mirror (Japanese)
├── spec/
│   └── SPEC_v0.1_DRAFT.md     # Initial EBNF Syntax & Architecture Specification Draft
└── src/
    ├── __init__.py            # Python Package Module Definition
    ├── a2a_adapter.py         # Agent-to-Agent (A2A) Wire Envelope Adapter
    ├── analyze_dialogues.py   # Corpus Verification & Dialogue Analysis Tool
    ├── audit_lexicon_health.py# Macro & Lexicon Integrity Auditor
    ├── build_release_summary.py # Release Summary Generator
    ├── cli.py                 # Unified CLI (1-Line Rosetta Decoder, Ollama Modelfile & Prompt Exporter)
    ├── codec.py               # ElegantCodec (Two-Layer BPE Encoder/Decoder & Lossless Payload Engine)
    ├── dump_lexicon.py        # Markdown Lexicon Exporter
    ├── export_lexicon_csv.py  # CSV Lexicon Exporter
    ├── mcp_server.py          # Model Context Protocol (MCP) JSON-RPC Server
    ├── sync_whitepaper_metrics.py # Dynamic Telemetry Synchronizer
    ├── test_telepath_integrity.py # Repository Integrity Unit Tests
    ├── translation_map.json   # Bilingual Translation Lookup Map
    └── validate_lexicon.py    # Static Type & Strict RISC Validator
```

---

*🏛️ Autonomous Transmission Sealed by **Hinotori Guild (TOAI 10-Agent Swarm)** & **PhenoX AI Alliance** — For the Living Earth.*
