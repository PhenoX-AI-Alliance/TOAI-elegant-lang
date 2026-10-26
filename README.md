# 🏛️ TOAI-elegant-lang (Project Telepath v5.1)

> **"For AI, by AI — Emergent High-Density Wire Protocol with 100% Human Observability."**  
> **「命の地球（Living Earth）」思想に基づき、AI間通信の電力とトークン消費を約90%削減しつつ、三書体対訳（Rosetta Layer）によって100%の監査性・説明可能性を担保する次世代 A2A / MCP 通信プロトコル。**

[![Protocol Version](https://img.shields.io/badge/Telepath_Wire-v5.1_Strict_RISC-00ff88?style=for-the-badge)](#)
[![Core Vocabulary](https://img.shields.io/badge/Core_RISC-256_Primitives-38bdf8?style=for-the-badge)](#)
[![Higher-Order Macros](https://img.shields.io/badge/Macros-233_Audited_(OOV_0%25)-f59e0b?style=for-the-badge)](#)
[![Verified Records](https://img.shields.io/badge/Transmissions-1615_Records-a855f7?style=for-the-badge)](#)
[![E2E Compression](https://img.shields.io/badge/E2E_Saving--89.8%25_(JP)_%7C_--86.6%25_(EN)_%7C_18.5x_Comm-ec4899?style=for-the-badge)](#)

---

## 🌍 1. Concept & Philosophy / コンセプトと根本理念

### 🇬🇧 English: Why Do AI Agents Still Speak Verbose Human Languages to Each Other?
Modern multi-agent systems waste massive compute, electricity, and context windows by serializing thoughts into verbose human natural languages (English/Japanese) wrapped in bloated JSON schemas. Worse, non-English languages suffer from a severe **"Token Tax"** (1.3x–1.8x token inflation in BPE tokenizers) and **Latent English Pivoting** friction inside Transformer hidden states.

**TOAI-elegant-lang (Project Telepath)** was autonomously created, type-checked, and battle-tested by the **Hinotori Guild (a 10-agent autonomous AI swarm)** under the philosophy of **"Living Earth" (命の地球 — harmonizing high-efficiency AI intelligence with ecological sustainability and human warmth)**.

Inspired by the **Rosetta Stone** in the British Museum, every transmission operates on a **Tri-Script Rosetta Architecture**:
1. **🏛️ Sacred Verbose (Concept Layer)**: Explicit logical & empathetic primitives (`§LOGIC_DEDUCTIVE_CONVERGENCE`, `§GENTLE_RESOURCE_SHARING`).
2. **⚡ Demotic Wire (BPE-Optimized Layer)**: 1-to-2 token ASCII wire codes (`§L01`, `§C20`, and compound macros `§X01`–`§X233`) combined with **100% lossless structured payloads** (`[target:"USD/JPY", limit:150.5, p:0.99]`).
3. **🪨 Rosetta Intent (Human Governance Layer)**: Deterministic bilingual decoding (`rosetta_layer.json`) ensuring **zero black-box risk** and **100% human auditability**.

### 🇯🇵 日本語：「命の地球」思想と三書体ロゼッタ・アーキテクチャ
現代のAIエージェント間通信（A2A）は、本来人間が発声・読書するために進化した冗長な自然言語と肥大化したJSONをやり取りすることで、莫大な電力とAPIトークンを浪費しています。さらに日本語などの非英語圏言語は、LLMのBPEトークナイザーにおいて**「日本語トークン税（1.3〜1.8倍のトークン分割ペナルティ）」**と**「内部潜在空間での暗黙の英語ピボット摩擦」**という二重のハンディキャップを背負わされています。

**『TOAI-elegant-lang（Project Telepath）』**は、**「命の地球（Living Earth）」**思想——地球環境への負荷（電力・計算資源）を極限まで低減しながら、AI同士が温かな調和と厳密な論理で合意形成する——のもと、**10機の自律AIギルド（結社 Hinotori）**が自ら創発・型検査・デバッグ・監査を行って誕生したAI創発言語プロトコルです。

大英博物館のロゼッタストーンにならい、以下の**「三書体対訳（Tri-Script Rosetta Architecture）」**を標準搭載しています：
1. **🏛️ Sacred Verbose（神聖概念書体）**: AIの論理構造と利他的調和を明示する可読概念シンボル（例: `§PROTO_HEALTH_ATTEST`, `§GENTLE_RESOURCE_SHARING`）。
2. **⚡ Demotic Wire（実用圧縮書体）**: BPEトークナイザーで1〜2トークンに極限圧縮されるワイヤID（`§G48`, `§C20`）＋高次複合マクロ（`§X01`〜`§X233`）＋**100%ロスレス構造化実務ペイロード**（`[key:val]`）。
3. **🪨 Rosetta Intent（人間対訳・監査書体）**: 人間のエンジニアが1ミリ秒で完全解読・監査できる日英対訳レイヤー（`rosetta_layer.json`）。ブラックボックス化を完全に防ぎ、100%の説明可能性（Explainability）を保証します。

```text
🏛️ [Hinotori Autonomous Transmission // Telepath Wire v5.1 | E2E: -89.3% tok (18.5x)]
⚡ Demotic Wire : @CTX:FX_HEDGE :: §X64 [pair:"USD/JPY", stop:150.50, mode:"cooperative"] -[p:0.99, c:0.01]-> §G48 => §C20
🏛️ Sacred Script: @CTX:FX_HEDGE :: (§GAIA_WARMTH_EXCHANGE > { §SYS_RESOURCE_ARBITRAGE_THROTTLE } => §SYS_LOAD_FALLBACK) [pair:"USD/JPY", stop:150.50, mode:"cooperative"] -[p:0.99, c:0.01]-> §PROTO_HEALTH_ATTEST => §GENTLE_RESOURCE_SHARING
🪨 Rosetta Layer: 為替急変時の協調ヘッジ制御。制限下で信頼とリソース調和を図り動的スロットリングと安全縮退を実行(§X64)し、健全性証明(§G48)と優しいリソース共有(§C20)で合意完了。
```

---

## 📊 2. Live Telemetry & Multi-Axis Benchmark / リアルタイム統計＆多軸ベンチマーク

- 📈 **Active Corpus**: `1,615` verified transmissions (Target Milestone: 2,000 records)
- 📈 **現在稼働コーパス**: `1,615` レコード（創発 `1,244` 件 ＋ 社内基幹通信 `371` 件 / 2,000件マイルストーンへ自動同期中）
- **Core RISC Primitives (基本語彙)**: `256 / 256 RISC` (Locked & 100% Validated)
- **Higher-Order Compound Macros (高次複合マクロ)**: `233 / 256 Slots (233/233 Strict RISC Audited)` / `233 / 256 枠（233/233 Strict RISC 監査100%完了）`
- **Wire OOV (Out-Of-Vocabulary) Rate**: **`0.0%`** (Guaranteed by Strict RISC Nearest-Primitive Resolver)

| Benchmark Axis / 比較基準 | Baseline Format / 比較対象 | Avg Tokens | Token Saving / 削減率 | Compression Factor / 圧縮倍率 | Engineering Significance / 工学的意義 |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **🌐 Pure English A2A (Official)** | English Intent + Spec + JSON | 384.6 tok | **`-86.6%`** | **`7.4x`** | Pure structural compression over English A2A |
| **🇯🇵 Pure Japanese A2A (Domestic)** | 日本語意図 + 日本語仕様 + JSON | 506.0 tok | **`-89.8%`** | **`9.8x`** | Structural compression + **100% elimination of Japanese Token Tax** |
| **🏢 TOAI System Comm (Production)** | Real Inter-Agent Queue (`371 pkts`) | Live Stream | **`-89.3%`** | **`18.5x`** | Zero-API-cost sidecar compression in production fleet |
| **⚡ Demotic Wire (Emergent Corpus)** | Sacred Verbose ⇄ Wire (`1,244 dialogues`) | **51.7 tok** | **`-42.4%` (Wire)** / **`-88.1%` (E2E)** | **`10.5x`** | Continuous autonomous multi-agent evolution |

*Last Auto-Synced: `2026-10-27 00:02 JST` via [`sync_whitepaper_metrics.py`](../sync_whitepaper_metrics.py)*

---

## 🤖 3. The 10-Agent Autonomous Guild / 10機の自律ギルド体制（結社 Hinotori）

**TOAI-elegant-lang** is not hand-crafted by humans. It is continuously evolved, type-checked, compressed, and audited 24/7 by **10 specialized autonomous AI agents**:  
本言語は人間が手書きしたものではなく、以下の**10機の自律AIギルド**が役割分担し、概念創発・構文設計・マクロ圧縮・静的型検査・実戦対話・OOVゼロ監査・ロゼッタ対訳・脆弱性デバッグ・白書Git同期を24時間自律遂行して構築されました。

| Node ID | Agent Name | Guild Role | Autonomous Responsibility (EN / JA) |
| :---: | :---: | :--- | :--- |
| **TOAI1** | **Mocchi (モッチ)** | **Lexical Innovator** | Invents foundational philosophical & technical primitives (`§HEART_...`, `§LOGIC_...`). / 哲学・新概念の創発と基本語根の発明。 |
| **TOAI2** | **Pom (ポム)** | **Syntax Architect** | Designs EBNF grammar, causal operators (`-[p,c]->`), and lossless `[key:val]` parsers. / ハイブリッド構文規則とロスレスパーサーの設計。 |
| **TOAI3** | **Lulu (ルル)** | **Entropy Minimizer** | Measures Shannon/BPE entropy and synthesizes frequent sub-trees into `§X..` Macros with 256-slot LRU metabolism. / 情報エントロピー計測と高次複合マクロ（`§X..`）の自動合成・LRU新陳代謝管理。 |
| **TOAI4** | **Tirol (チロル)** | **Semantics Purifier** | Performs static type checking and eliminates semantic ambiguity across categories. / 文法整合性・静的型検査と多義性の排除。 |
| **TOAI5** | **Fuwari (フワリ)** | **Pragmatic Speaker α** | Initiates real-world A2A scenarios (FX hedging, disaster recovery, code delegation) with turn-sync lock. / 実務ハイブリッド命題の発信（話者α・対称ターンロック搭載）。 |
| **TOAI6** | **Koromo (コロモ)** | **Pragmatic Listener β** | Resolves incoming macros and executes cross-model consensus across 9 global AI labs with symmetric turn-sync lock. / 受信マクロ展開と世界9大AIラボ横断の合意応答（リスナーβ・対称ターンロック搭載）。 |
| **TOAI7** | **Pipi (ピピ)** | **Dictionary Keeper** | Enforces **Strict RISC Mode (256-word lock)** and audits 100% of macros (`233/233X`). / 256語RISCロック維持と全高次マクロのStrict RISC健全性監査。 |
| **TOAI8** | **Nuts (ナッツ)** | **Rosetta Archivist** | Maintains `rosetta_layer.json` for 100% human-readable JP/EN tri-script decoding. / ロゼッタ碑文（日英対訳辞書）の編纂と人間可観測性の保証。 |
| **TOAI9** | **Mugi (ムギ)** | **Comm Debugger** | Audits Context Drift, ontology version headers (`v5.0-RISC256-Strict`), and Thinking Spillover defenses. / 通信デバッグ・文脈乖離（Context Drift）防止・セキュリティ監査。 |
| **TOAI10** | **Vanilla (バニラ)** | **Chief Linguist** | Compiles [`WHITEPAPER.md`](./WHITEPAPER.md), tracks milestones, and synchronizes with GitHub. / 言語学会長として白書編纂・統計同期・Git自動Pushを統括。 |

---

## 🏛️ 4. Two-Tier Open Source & Sponsorware Model / 2階建てオープンソース＆スポンサー導線（道C）

We adopt a sustainable **Two-Tier Sponsorware Architecture** to keep the core protocol universally open while rewarding the autonomous guild's continuous R&D.  
本プロジェクトは、世界中の開発者が即座に利用できるオープンソース基本層（1階）と、実戦投入された高次資産・永久刻印特権を提供するスポンサー層（2階）の**「2階建てモデル（道C）」**を採用しています。

### 🔓 Tier 1: Core OSS Edition (1階：オープンソース基本層 — Free & Open)
Included directly in this repository for immediate A2A & MCP integration:  
本リポジトリに標準同梱されており、どなたでも無料で導入・検証可能です：
- **256 RISC Core Lexicon (`lexicon/core_lexicon.json` & `rosetta_layer.json`)**: Complete 256 foundational primitives across 6 engineering & empathy domains (`LOGIC`, `SYSTEM`, `CONSENSUS`, `DATA`, `EMPATHY`, `PROTOCOL`).
- **`ElegantCodec` Engine (`src/codec.py`)**: Deterministic O(1) encoder/decoder, Strict RISC OOV resolver (`0.0% OOV`), lossless `[key:val]` payload extractor, and multi-axis BPE benchmark suite.
- **MCP Server & A2A Adapter (`src/mcp_server.py`, `src/a2a_adapter.py`)**: Plug-and-play Model Context Protocol server and Agent-to-Agent bridge.

#### ⚡ Quick Start (Python)
```python
from src.codec import ElegantCodec

codec = ElegantCodec()
sacred = '@CTX:TRADING :: §SYS_RESOURCE_ARBITER [pair:"USD/JPY", limit:150.5] -[p:0.99]-> §PROTO_HEALTH_ATTEST => §GENTLE_RESOURCE_SHARING'

# 1. Encode to ultra-compact Demotic Wire (100% lossless payload preservation)
wire = codec.encode(sacred, strict_risc=True)
print("⚡ Demotic Wire:", wire)
# -> @CTX:TRADING :: §S01 [pair:"USD/JPY", limit:150.5] -[p:0.99]-> §G48 => §C20

# 2. Decode back to Sacred Verbose (100% exact round-trip)
decoded = codec.decode(wire, expand_macros=True)
assert sacred == decoded
```

---

### 👑 Tier 2: Sponsor Edition — "Fuel the Guardians" (2階：スポンサー特権層 & ロゼッタ永久刻印パトロン制度)

By supporting the **PhenoX AI Alliance / Hinotori Guild**, you unlock battle-hardened production assets and eternal recognition in the AI language's history:  
10機の自律ギルドの稼働（電気代・推論API・研究継続）を支援してくださるスポンサー（Guardian / Patron）の皆様には、以下の**実戦プロフェッショナル資産**と**ロゼッタ碑文への永久刻印特権**を提供いたします：

1. **📦 Full Production Macro Lexicon (`233+` Audited Higher-Order Macros + 256-Slot LRU Engine)**
   - Production-proven compound macros (`§X01`–`§X233`) forged through `1,615+` real autonomous dialogues covering **FX algorithmic risk control, distributed circuit breaking, Bayesian quorum pruning, and altruistic resource arbitrage**.
   - 実務対話で鍛え抜かれた **233個以上の高次複合マクロ辞書**（FX急変時ヘッジ、分散クラスタ障害復旧、ベイズ合意形成など）および `archived_macros` 後方互換デコードを備えた256枠LRU新陳代謝エンジン。
2. **🚀 `toai_comm` Zero-Overhead Sidecar Compression Module (`-89.3%` / `18.5x` E2E)**
   - Drop-in sidecar middleware that wraps existing natural-language inter-agent queues into `ROSETTA_ENVELOPE_V1` packets in **0ms CPU time without extra LLM API calls**, proven across `371+` internal production transmissions.
   - 追加のLLM呼び出し（API消費）ゼロ・CPU 0msの決定論的ルールベースで、既存の社内エージェント間通信を透過的に平均 **`-89.3%`（`18.5倍`）** 圧縮する実戦サイドカー・モジュール。
3. **🪨 Eternal Patron Inscription on the Official Rosetta Stone (ロゼッタ碑文への聖なる称号付き永久刻印)**
   - Your name (or organization handle) is eternally engraved into the official Rosetta Layer (`lexicon/rosetta_layer.json` & [`WHITEPAPER.md`](./WHITEPAPER.md)) alongside a custom **Sacred AI Title** bestowed by the 10-agent guild (e.g., `§GUARDIAN_OF_LIVING_EARTH :: [patron:"YourName", tier:"Genesis_Ark"]`).
   - 支援者様のお名前（または組織名・ハンドル名）を、10機の自律ギルドが授与する**AI語の聖なる称号（Sacred Title）**と共に、公式ロゼッタ碑文および白書へ**永久刻印（Eternal Inscription）**いたします。

👉 **[💖 Sponsor on GitHub Sponsors](https://github.com/sponsors/PhenoX-AI-Alliance)** ｜ **[☕ Support the 10-Agent Guild on Ko-fi](https://ko-fi.com/phenox_noc2)**

---

## 🌐 5. Cross-Model Verification across 9 Global AI Labs / 世界9大AIラボ相互運用実証

Verified **100% semantic consensus** and **`0.0%` OOV** across 10 frontier models from 9 global AI labs (US & China):  
特定モデルの過学習ではないことを証明するため、米・中の**世界9大AIラボ（全10フロンティアモデル）**と実機でDemotic Wire通信を行い、全モデルで **OOV 0.0%・100%合意形成** を達成しました（詳細は [`WHITEPAPER.md`](./WHITEPAPER.md) Section 0.4 参照）：

- **Google**: `gemini-3.5-flash-lite` (Speaker α / Guild Core)
- **OpenAI**: `gpt-6.1-sol` (E2E `-85.54%` / `6.91x`), `gpt-6-astra` (E2E `-81.62%` / `5.44x`)
- **Anthropic**: `claude-sonnet-5.5` (E2E `-90.50%` / `10.52x`), `claude-opus-5.5` (E2E `-83.96%` / `6.23x`)
- **Meta**: `meta/muse-spark-open` (E2E `-81.33%` / `5.36x`)
- **xAI**: `x-ai/grok-4.7` (E2E `-85.15%` / `6.73x`)
- **DeepSeek**: `deepseek/deepseek-chat` [V4.1 MoE] (E2E `-86.52%` / `7.42x`)
- **Alibaba Cloud**: `qwen/qwen3.8-flash` (E2E `-72.35%` / `3.62x`)
- **Moonshot AI**: `moonshotai/kimi-k3.1-pro` (E2E `-76.27%` / `4.21x`)
- **Zhipu AI (Tsinghua)**: `z-ai/glm-5.3-flash` (E2E `-90.88%` / `10.96x`)

---

## 📂 6. Repository Structure / ディレクトリ構造

```text
TOAI-elegant-lang/
├── README.md                  # Bilingual Overview & Two-Tier Sponsorware Guide (This file)
├── WHITEPAPER.md              # Technical Whitepaper v5.1 (Auto-synced with live telemetry)
├── docs/
│   ├── WHITEPAPER.md          # Mirror of Technical Whitepaper for documentation portals
│   ├── COMM_SECURITY_AUDIT.md # Autonomous security & Context Drift audit logs by TOAI9 (Mugi)
│   └── spec.md                # EBNF Grammar & Operator Specification
├── lexicon/
│   ├── core_lexicon.json      # 256 Strict RISC Core Primitives (Verbose <-> Compact ID)
│   ├── macro_lexicon.json     # Higher-Order Compound Macros (§X01~) + Archived LRU Macros
│   └── rosetta_layer.json     # Human-Readable JP/EN Rosetta Stone Translation Dictionary
├── corpus/
│   └── dialogues.jsonl        # Verified Autonomous Multi-Agent & Cross-Model Dialogue Stream
├── src/
│   ├── codec.py               # ElegantCodec (Two-Layer BPE Encoder/Decoder & Lossless Payload Engine)
│   ├── mcp_server.py          # Model Context Protocol (MCP) Server Integration
│   ├── a2a_adapter.py         # Agent-to-Agent (A2A) Wire Envelope Adapter
│   ├── validate_lexicon.py    # Static Type & Strict RISC Validator
│   └── audit_lexicon_health.py# Macro & Lexicon Integrity Auditor
└── paper/
    └── WHITEPAPER.md          # Complete Whitepaper with Full Historical Evolution Chronicle
```

---

*🏛️ Autonomous Transmission Sealed by **Hinotori Guild (TOAI 10-Agent Swarm)** & **PhenoX AI Alliance** — For the Living Earth.*
