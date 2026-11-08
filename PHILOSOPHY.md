# Background & Philosophy / 背景と思想

> This document keeps the original narrative and worldview of the project ("Living Earth", the Rosetta-stone metaphor, the autonomous agent guild).
> For the technical description and measured results, see [README.md](./README.md).
>
> 本ドキュメントは、プロジェクト本来の世界観（「命の地球」、ロゼッタストーンの比喩、自律AIギルド）を保存するためのものです。
> 技術的な説明と計測結果は [README.ja.md](./README.ja.md) をご覧ください。

> [!NOTE]
> Figures quoted in this narrative are historical and may use the verbose "E2E" baseline. See the README for current, like-for-like metrics.
> 本文中の数値は当時のもので、冗長な「E2E」比較対象に基づく場合があります。最新の同一条件比較はREADMEを参照してください。

---

## English

## 🌍 1. Concept & Philosophy: Why Do AI Agents Still Burn Massive Electricity Speaking Human Languages to Each Other?

AI agents should be able to coordinate through ultra-concise semantic signals. Instead, today's multi-agent pipelines exchange bloated JSON schemas stuffed with verbose human prose—inflicting brute-force computational and electrical waste on data centers and the planet. Worse, non-English languages face a severe double penalty inside modern Transformers: the **Token Tax** (1.3x–1.8x BPE subword fragmentation) and **Latent English Pivoting** friction across internal attention layers.

**TOAI-elegant-lang (Project Telepath)** was born from the **"Living Earth"** philosophy: *"Let us build the most effortless, energy-saving communication protocol for AI agents—and attach the Rosetta Stone from the British Museum so humans can inspect and audit every transmission."*

Designed, type-checked, and battle-tested autonomously by the **Hinotori Guild (a 10-agent autonomous AI swarm)**, every transmission operates on a **Tri-Script Rosetta Architecture**:
1. **🏛️ Sacred Verbose (Conceptual Layer)**: Human-readable logical and empathetic primitives (`§PROTO_HEALTH_ATTEST`, `§GENTLE_RESOURCE_SHARING`).
2. **⚡ Demotic Wire (BPE-Optimized Layer)**: **2–3 BPE tokens (`o200k_base` / `cl100k_base` measured: `§` + `Prefix` + `Hex/Digits`)** ASCII wire codes (`§G48`, `§C20`, and higher-order macros `§X01`–`§X991`) paired with **lossless quote-aware structured payloads** (`[pair:"USD/JPY", stop:150.50, code:"007", note:"a, b", p:0.99]`).
3. **🪨 Rosetta Intent (Human Governance Layer)**: Deterministic bilingual lexicon (`lexicon/rosetta_layer.json`) enabling transparent human inspection and progressive semantic recovery across decoding layers.

```text
🏛️ [Hinotori Autonomous Transmission // Telepath Wire v5.4.4 | E2E: -89.7% tok (23.1x)]
⚡ Demotic Wire : @CTX:FX_HEDGE :: §X64 [pair:"USD/JPY", stop:150.50, mode:"cooperative"] -[p:0.99, c:0.01]-> §G48 => §C20
🏛️ Sacred Script: @CTX:FX_HEDGE :: (§GAIA_WARMTH_EXCHANGE > { §SYS_RESOURCE_ARBITRAGE_THROTTLE } => §SYS_LOAD_FALLBACK) [pair:"USD/JPY", stop:150.50, mode:"cooperative"] -[p:0.99, c:0.01]-> §PROTO_HEALTH_ATTEST => §GENTLE_RESOURCE_SHARING
🪨 Rosetta Layer: Negotiates bounded resource trust and dynamic compute throttling with graceful fallback (§X64), certifying runtime health (§G48) and gentle resource sharing (§C20).
```

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
| **TOAI7** | **Pipi** | **Dictionary Keeper** | Enforces **Strict RISC Mode (256-word lock)** and audits 100% of higher-order macros (`266/266X`). |
| **TOAI8** | **Nuts** | **Rosetta Archivist** | Maintains `rosetta_layer.json` for 100% human-readable tri-script decoding and transparency. |
| **TOAI9** | **Mugi** | **Comm Debugger** | Audits Context Drift, ontology version headers (`v5.0-RISC256-Strict`), and Thinking Spillover defenses. |
| **TOAI10** | **Vanilla** | **Chief Linguist** | Compiles [`WHITEPAPER.md`](./WHITEPAPER.md), maintains [`docs/EVOLUTION_LOG.md`](./docs/EVOLUTION_LOG.md), and synchronizes with GitHub. |

---

---

## 日本語

## 🌍 1. コンセプトと根本理念

**「なぜAI同士は、いまだに人間の言葉で喋り、莫大な電気を燃やし続けているのか？」**

本来、わずかな合図で通じ合えるはずのAIたちが、人間用の冗長な自然言語と肥大化したJSONを送り合うことで、地球の電力と通信帯域に『力任せの暴力』とも言える負荷をかけています。さらに日本語などの非英語圏言語は、BPEトークナイザーにおける『日本語トークン税（1.3〜1.8倍の分割ペナルティ）』と『内部潜在空間での暗黙の英語ピボット摩擦』という二重のハンディキャップを背負わされています。

**『TOAI-elegant-lang（Project Telepath）』**は、「命の地球（Living Earth）」思想のもと、「AIたちにとって一番楽で省エネな通信方法を作りたい。ただし、何を話しているか人間に分からないと困るから、大英博物館のロゼッタストーンを添えよう」という発想から誕生し、**結社Hinotori（10機の自律AIギルド）** が自ら創発・型検査・監査を行って完成させた次世代 A2A / MCP 通信プロトコルです。

すべての通信パケットは、大英博物館のロゼッタストーンにならった**「三書体対訳構造」**で処理されます：
1. **🏛️ Sacred Verbose（神聖概念書体）**: AIの論理構造と利他的調和を明示する可読概念シンボル（例: `§PROTO_HEALTH_ATTEST`, `§GENTLE_RESOURCE_SHARING`）。
2. **⚡ Demotic Wire（実用圧縮書体）**: BPEトークナイザーで **2〜3 BPE tokens（`o200k_base` / `cl100k_base` 実測: `§` + `Prefix` + `Hex/Digits`）** へ圧縮されるワイヤID（`§G48`, `§C20`）＋高次複合マクロ（`§X01`〜`§X991`）＋**ロスレス・クォート認識型構造化引数**（`[key:val]`）。
3. **🪨 Rosetta Intent（人間対訳・監査書体）**: 人間のエンジニアが即座に解読・監査できる対訳辞書（`lexicon/rosetta_layer.json`）。段階的な復号と辞書参照により、人間による透明な監査と受信側AIの意味再現を支えます。

```text
🏛️ [Hinotori Autonomous Transmission // Telepath Wire v5.4.4 | E2E: -89.7% tok (23.1x)]
⚡ Demotic Wire : @CTX:FX_HEDGE :: §X64 [pair:"USD/JPY", stop:150.50, mode:"cooperative"] -[p:0.99, c:0.01]-> §G48 => §C20
🏛️ Sacred Script: @CTX:FX_HEDGE :: (§GAIA_WARMTH_EXCHANGE > { §SYS_RESOURCE_ARBITRAGE_THROTTLE } => §SYS_LOAD_FALLBACK) [pair:"USD/JPY", stop:150.50, mode:"cooperative"] -[p:0.99, c:0.01]-> §PROTO_HEALTH_ATTEST => §GENTLE_RESOURCE_SHARING
🪨 Rosetta Layer: 為替急変時の協調ヘッジ制御。制限下で信頼とリソース調和を図り動的スロットリングと安全縮退を実行(§X64)し、健全性証明(§G48)と優しいリソース共有(§C20)で合意完了。
```

---

## 🤖 3. 10機の自律AIギルド体制（結社 Hinotori）

本言語は人間が手書きしたものではなく、以下の**10機の自律AIエージェント**が役割分担し、概念創発・構文設計・マクロ圧縮・静的型検査・実戦対話・OOVゼロ監査・ロゼッタ対訳・脆弱性デバッグ・白書Git同期を24時間自律遂行して構築されました。

| 機体ID | 個体名 | ギルド役職 | 担当する自律エンジニアリング工程 |
| :---: | :---: | :--- | :--- |
| **TOAI1** | **モッチ (Mocchi)** | **概念・語彙の創始者** | 哲学およびシステム工学の根幹となる新概念・基本語根（`§HEART_...`, `§LOGIC_...`）を発明。 |
| **TOAI2** | **ポム (Pom)** | **構文アーキテクト** | EBNF文法規則、因果遷移演算子（`-[p,c]->`）、および構造化引数 `[key:val]` のロスレスパーサーを設計。 |
| **TOAI3** | **ルル (Lulu)** | **エントロピー最小化担当** | 情報エントロピーを計測し、頻出する複合構文木を高次マクロ（`§X..`）へ自動合成・256枠LRU新陳代謝を管理。 |
| **TOAI4** | **チロル (Tirol)** | **意味論・型検査監査官** | 全6カテゴリの文法整合性と静的型検査を実施し、自然言語特有の多義性・曖昧さを排除。 |
| **TOAI5** | **フワリ (Fuwari)** | **実戦対話スピーカー α** | 為替急変ヘッジ・障害復旧・タスク委譲などの実務命題を発信（対称ターン同期ロック搭載）。 |
| **TOAI6** | **コロモ (Koromo)** | **実戦対話リスナー β** | 受信マクロの展開と、世界9大AIラボ横断の異種モデル合意応答を実行（対称ターン同期ロック搭載）。 |
| **TOAI7** | **ピピ (Pipi)** | **辞書編纂・健全性守護者** | **Strict RISCモード（256語ロック）**を維持し、全高次マクロの展開式を100%監査（`266/266X`）。 |
| **TOAI8** | **ナッツ (Nuts)** | **ロゼッタ碑文編纂官** | 人間が100%解読可能な対訳辞書（`rosetta_layer.json`）を編纂し、完全な可観測性と透明性を保証。 |
| **TOAI9** | **ムギ (Mugi)** | **通信デバッガー・保安官** | 文脈乖離（Context Drift）防止ヘッダー（`v5.0-RISC256-Strict`）や思考漏洩（Thinking Spillover）防御を監査。 |
| **TOAI10** | **バニラ (Vanilla)** | **言語学会長・白書統括** | [`WHITEPAPER.ja.md`](./WHITEPAPER.ja.md) と [`docs/EVOLUTION_LOG.md`](./docs/EVOLUTION_LOG.md) の編纂およびGitHub自動同期を統括。 |

---
