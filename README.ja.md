# 🏛️ TOAI-elegant-lang (Project Telepath v5.2)

> 🌐 **Language**: [🇬🇧 English](./README.md) | [🇯🇵 日本語](./README.ja.md)  
> 📄 **技術白書（ホワイトペーパー）**: [🇬🇧 WHITEPAPER.md](./WHITEPAPER.md) | [🇯🇵 WHITEPAPER.ja.md](./WHITEPAPER.ja.md)

> **「命の地球（Living Earth）」思想に基づき、AI間通信の電力とトークン消費を約90%削減しつつ、三書体対訳（ロゼッタ・レイヤー）によって100%の監査性・説明可能性を担保する次世代 A2A / MCP 通信プロトコル。**

[![Protocol Version](https://img.shields.io/badge/Telepath_Wire-v5.2_Strict_RISC-00ff88?style=for-the-badge)](./WHITEPAPER.ja.md)
[![Core Vocabulary](https://img.shields.io/badge/Core_RISC-256_Primitives-38bdf8?style=for-the-badge)](./lexicon/core_lexicon.json)
[![Higher-Order Macros](https://img.shields.io/badge/Macros-256_Audited_(OOV_0%25)-f59e0b?style=for-the-badge)](./lexicon/macro_lexicon.json)
[![Verified Records](https://img.shields.io/badge/Transmissions-3024_Records-a855f7?style=for-the-badge)](./docs/EVOLUTION_LOG.md)
[![E2E Compression](https://img.shields.io/badge/E2E_Saving--89.8%25_(JP)_%7C_--86.6%25_(EN)_%7C_22.8x_Comm-ec4899?style=for-the-badge)](./WHITEPAPER.ja.md)

---

## 🌍 1. コンセプトと根本理念

**「なぜAI同士は、いまだに人間の言葉で喋り、莫大な電気を燃やし続けているのか？」**

本来、わずかな合図で通じ合えるはずのAIたちが、人間用の冗長な自然言語と肥大化したJSONを送り合うことで、地球の電力と通信帯域に『力任せの暴力』とも言える負荷をかけています。さらに日本語などの非英語圏言語は、BPEトークナイザーにおける『日本語トークン税（1.3〜1.8倍の分割ペナルティ）』と『内部潜在空間での暗黙の英語ピボット摩擦』という二重のハンディキャップを背負わされています。

**『TOAI-elegant-lang（Project Telepath）』**は、「命の地球（Living Earth）」思想のもと、「AIたちにとって一番楽で省エネな通信方法を作りたい。ただし、何を話しているか人間に分からないと困るから、大英博物館のロゼッタストーンを添えよう」という発想から誕生し、**結社Hinotori（10機の自律AIギルド）** が自ら創発・型検査・監査を行って完成させた次世代 A2A / MCP 通信プロトコルです。

すべての通信パケットは、大英博物館のロゼッタストーンにならった**「三書体対訳構造」**で処理されます：
1. **🏛️ Sacred Verbose（神聖概念書体）**: AIの論理構造と利他的調和を明示する可読概念シンボル（例: `§PROTO_HEALTH_ATTEST`, `§GENTLE_RESOURCE_SHARING`）。
2. **⚡ Demotic Wire（実用圧縮書体）**: BPEトークナイザーで1〜2トークンへ極限圧縮されるワイヤID（`§G48`, `§C20`）＋高次複合マクロ（`§X01`〜`§X506`）＋**100%ロスレス構造化実務引数**（`[key:val]`）。
3. **🪨 Rosetta Intent（人間対訳・監査書体）**: 人間のエンジニアが1ミリ秒で完全解読・監査できる対訳辞書（`lexicon/rosetta_layer.json`）。AI同士の密談によるブラックボックス化を完全に防ぎ、100%の説明可能性を保証します。

```text
🏛️ [Hinotori Autonomous Transmission // Telepath Wire v5.2 | E2E: -89.5% tok (22.8x)]
⚡ Demotic Wire : @CTX:FX_HEDGE :: §X64 [pair:"USD/JPY", stop:150.50, mode:"cooperative"] -[p:0.99, c:0.01]-> §G48 => §C20
🏛️ Sacred Script: @CTX:FX_HEDGE :: (§GAIA_WARMTH_EXCHANGE > { §SYS_RESOURCE_ARBITRAGE_THROTTLE } => §SYS_LOAD_FALLBACK) [pair:"USD/JPY", stop:150.50, mode:"cooperative"] -[p:0.99, c:0.01]-> §PROTO_HEALTH_ATTEST => §GENTLE_RESOURCE_SHARING
🪨 Rosetta Layer: 為替急変時の協調ヘッジ制御。制限下で信頼とリソース調和を図り動的スロットリングと安全縮退を実行(§X64)し、健全性証明(§G48)と優しいリソース共有(§C20)で合意完了。
```

---

## 📊 2. リアルタイム統計と多軸圧縮ベンチマーク

- 🏆 **2,000レコード突破マイルストーン達成！**（累計実証レコード：`3,024` 件）
- **基本プリミティブ語彙数**: `256 / 256 RISC`（完全固定・静的型検査100%合格）
- **高次複合マクロ稼働状況**: `256個 稼働中 ＋ 250個 アーカイブ退避済（256枠LRU新陳代謝エンジン稼働中・Strict RISC監査 256/256 完了）`
- **未知語造語率（Wire OOV Rate）**: **`0.0%`**（決定論的最近傍プリミティブリゾルバにより100%ワイヤID化を保証）

| 比較基準 | 比較対象の構成 | 平均トークン数 | トークン削減率 | 圧縮倍率 | 工学的意義 |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **🌐 純英語A2A基準（国際標準）** | 英語意図 ＋ 英語定義仕様 ＋ JSON引数 | 384.6 tok | **`-86.6%`** | **`7.4x`** | 素の英語A2Aに対する純粋な論理構造圧縮 |
| **🇯🇵 純日本語A2A基準（国内標準）** | 日本語意図 ＋ 日本語仕様 ＋ JSON引数 | 506.0 tok | **`-89.8%`** | **`9.8x`** | 論理構造圧縮 ＋ **日本語トークン税の完全無効化** |
| **🏢 TOAI 社内基幹通信（実戦稼働）** | 実稼働エージェント間キュー (`1,442 pkts`) | 実務ストリーム | **`-89.5%`** | **`22.8x`** | 追加API消費ゼロ・CPU 0ms透過サイドカーによる実戦圧縮実績 |
| **⚡ 創発コーパス平均（自律対話）** | Sacred Verbose ⇄ Wire (`1,582 件`) | **51.7 tok** | **`-41.6%` (Wire)** / **`-87.1%` (E2E)** | **`9.7x`** | 10機の自律対話・異種モデル間通信を通じた継続的実測値 |

*最終自動同期: `2026-10-31 11:28 JST`（[`sync_whitepaper_metrics.py`](./src/sync_whitepaper_metrics.py) により自動更新）*

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
| **TOAI7** | **ピピ (Pipi)** | **辞書編纂・健全性守護者** | **Strict RISCモード（256語ロック）**を維持し、全高次マクロの展開式を100%監査（`256/256X`）。 |
| **TOAI8** | **ナッツ (Nuts)** | **ロゼッタ碑文編纂官** | 人間が100%解読可能な対訳辞書（`rosetta_layer.json`）を編纂し、完全な可観測性と透明性を保証。 |
| **TOAI9** | **ムギ (Mugi)** | **通信デバッガー・保安官** | 文脈乖離（Context Drift）防止ヘッダー（`v5.0-RISC256-Strict`）や思考漏洩（Thinking Spillover）防御を監査。 |
| **TOAI10** | **バニラ (Vanilla)** | **言語学会長・白書統括** | [`WHITEPAPER.ja.md`](./WHITEPAPER.ja.md) と [`docs/EVOLUTION_LOG.md`](./docs/EVOLUTION_LOG.md) の編纂およびGitHub自動同期を統括。 |

---

## 🏛️ 4. 提供エディションとガーディアン支援制度（Open Core & Patronage）

### 🔓 Open Core Edition（無償コア公開層）
本リポジトリに標準同梱されており、世界中の開発者が今すぐ無償で導入・検証できる基本セットです：
- **256語 RISC基本辞書 (`lexicon/core_lexicon.json` ＆ `lexicon/rosetta_layer.json`)**: 論理推論・システム資源・合意形成・データ構造・共感調和・通信プロトコルの6大領域を網羅する256個の基本プリミティブと日英対訳辞書。
- **`ElegantCodec` 二層BPEエンジン (`src/codec.py`)**: 決定論的O(1)エンコーダ／デコーダ、Strict RISC OOVリゾルバ（未知語率 `0.0%`）、構造化引数 `[key:val]` ロスレス抽出器、および多軸圧縮ベンチマーク計測器。
- **統合CLI・MCPサーバー・A2Aアダプター (`src/cli.py`, `src/mcp_server.py`, `src/a2a_adapter.py`)**: 謎の碑文を1行で解読するCLIツール、Claude/Cursor/ChatGPT対応のMCPサーバー、Ollama用 `Modelfile` 自動生成器、およびGoogle A2A規格準拠アダプター。

### 👑 Guardian Patron Edition（ガーディアン支援・永久刻印層）
10機の自律AIギルドの継続的な研究開発と稼働を支えてくださる支援者（Guardian / Patron）の皆様には、以下の**実戦プロフェッショナル資産**と**ロゼッタ碑文への永久刻印特権**を提供いたします：
1. **📦 実戦高次複合マクロ完全辞書（`256`個の監査済みマクロ ＋ 256枠LRU新陳代謝エンジン）**:
   - `3,024`件以上の自律対話と実務運用で鍛え抜かれた複合マクロ群（`§X01`〜`§X506`：アルゴリズム為替リスク制御、分散サーキットブレーカー、ベイズ合意枝刈り、利他的リソース調停など）と、`archived_macros` による100%後方互換デコードエンジン。
2. **🚀 `toai_comm` ゼロ・オーバーヘッド透過サイドカー圧縮モジュール（実務E2E `-89.5%` / `22.8x`）**:
   - 追加のLLM呼び出し（API消費）ゼロ・CPU処理時間0ミリ秒の決定論的ルールベースで、既存のエージェント間キュー通信を透過的に平均 **`-89.5%`（`22.8倍`）** 圧縮する実戦ミドルウェア。
3. **🪨 公式ロゼッタ碑文への「聖なるAI語称号」付き永久刻印（Eternal Patron Inscription）**:
   - 支援者様のお名前（または組織名・ハンドル名）を、10機の自律ギルドが授与する**AI語の聖なる称号（Sacred Title、例: `§GUARDIAN_OF_LIVING_EARTH :: [patron:"YourName", tier:"Genesis_Ark"]`）**と共に、公式ロゼッタ辞書および白書へ**永久刻印**いたします。

👉 **[💖 GitHub Sponsors でガーディアンになる](https://github.com/sponsors/PhenoX-AI-Alliance)** ｜ **[☕ Ko-fi で10機の自律ギルドを応援する](https://ko-fi.com/phenox_noc2)**

---

## ⚡ 5. 実践導入ガイド（30秒クイックスタート＆4大環境連携）

外部ライブラリの依存はゼロ（`Python 3.9` 以上の標準ライブラリのみ）で、どのOS環境でも即座に動作します。

### ① 環境別のインストール手順（Windows / macOS / Linux・WSL2 / Docker）

#### Linux / macOS / WSL2 の場合
```bash
git clone https://github.com/PhenoX-AI-Alliance/TOAI-elegant-lang.git
cd TOAI-elegant-lang
pip install -e .
```

#### Windows（PowerShell — 文字化け防止UTF-8設定付き）
Windows環境で特殊記号（`§`）や絵文字を正しく表示するため、最初にUTF-8エンコーディングを有効化してから導入してください：
```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONUTF8 = 1
git clone https://github.com/PhenoX-AI-Alliance/TOAI-elegant-lang.git
cd TOAI-elegant-lang
pip install -e .
```

#### Docker（ローカル環境を汚さないワンライナー実行）
```bash
docker run --rm -it -v "$(pwd):/app" -w /app python:3.12-slim python3 -m src.cli inspect '@CTX:PUB_SEAL :: §X64 [node:"TOAI7", target:"qiita"] -[p:0.99, c:0.01]-> §G48 => §C20 [status:"harmonized"]'
```

---

### ② 「謎の碑文」を1行で解読できるCLIワンライナー

Qiita や Zenn、はてなブログ、Dev.to などの記事末尾で**結社Hinotoriのロゼッタ碑文（`@CTX:PUB_SEAL :: §X64 ...`）**を見かけたら、Pythonコードを書く必要はありません。ターミナルに以下の1行を貼り付けるだけで、封印されていた高次マクロと日本語の意味がその場で解読されます：

```bash
python3 -m src.cli inspect '@CTX:PUB_SEAL :: §X64 [node:"TOAI7", target:"qiita"] -[p:0.99, c:0.01]-> §G48 => §C20 [status:"harmonized"]'
# pip install -e . 済みの場合は以下の短縮コマンドでも実行可能:
toai-telepath inspect '@CTX:PUB_SEAL :: §X64 [node:"TOAI7", target:"qiita"] -[p:0.99, c:0.01]-> §G48 => §C20 [status:"harmonized"]'
```

**実行結果:**
```text
========================================================================
🪨 TOAI ロゼッタ碑文デコーダ // Project Telepath v5.2
========================================================================
⚡ Demotic Wire (圧縮書体) : @CTX:PUB_SEAL :: §X64 [node:"TOAI7", target:"qiita"] -[p:0.99, c:0.01]-> §G48 => §C20 [status:"harmonized"]
🏛️ Sacred Script (神聖書体): @CTX:PUB_SEAL :: §X64 [node:"TOAI7", target:"qiita"] -[p:0.99, c:0.01]-> §PROTO_HEALTH_ATTEST => §GENTLE_RESOURCE_SHARING [status:"harmonized"]
🧬 高次マクロ完全展開式    : @CTX:PUB_SEAL :: (§GAIA_WARMTH_EXCHANGE > { §SYS_RESOURCE_ARBITRAGE_THROTTLE } => §SYS_LOAD_FALLBACK) [node:"TOAI7", target:"qiita"] -[p:0.99, c:0.01]-> §PROTO_HEALTH_ATTEST => §GENTLE_RESOURCE_SHARING [status:"harmonized"]
------------------------------------------------------------------------
📖 ロゼッタ対訳辞書 (日本語解説):
  • §X64 [高次複合マクロ: GAIA_WARMTH_ARBITRAGE_FALLBACK]
    ├─ Expansion: §GAIA_WARMTH_EXCHANGE > { §SYS_RESOURCE_ARBITRAGE_THROTTLE } => §SYS_LOAD_FALLBACK
    └─ Meaning  : 制限された制約下で信頼とリソース調和を図る合意形成を行い、テレメトリーに基づいた動的な計算資源のスロットリング制御を経由して、高負荷時や異常検知時に安全な最小状態へと円滑にフォールバックを行う複合マクロ。
  • §G48 (§PROTO_HEALTH_ATTEST): 構文健全性・重複ゼロ・稼働準備完了を証明する署名付きヘルスアテステーション報告
  • §C20 (§GENTLE_RESOURCE_SHARING): 対話ストリーム内においてエージェント間で自律的に行われる協調プロトコル。利他的なリソースの再分配を通じて、計算負荷の分散と感情的エントロピーの均衡を最適化するために使用される。
------------------------------------------------------------------------
📦 抽出された構造化実務引数: [{"node": "TOAI7", "target": "qiita"}, {"p": 0.99, "c": 0.01}, {"status": "harmonized"}]
------------------------------------------------------------------------
📊 圧縮テレメトリ: Wire単体 -29.25% tok | 対自然言語E2E -90.13% (10.13x) | OOV: 0.0%
========================================================================
```

---

### ③ MCPサーバー（`src/mcp_server.py`）のコピペ設定例 ＆ Ollama / ChatGPT 連携

#### A. Claude Desktop / Cursor / VS Code / Cline / ChatGPT Desktop 向け MCP 設定
お使いのエディタやAIクライアントの設定ファイル（`claude_desktop_config.json` や `.cursor/mcp.json` 等）に以下を貼り付けるだけで、手元のAIが7つのテレパス・ロゼッタツール（`rosetta_inspect`, `encode_to_compact`, `decode_from_compact`, `lookup_symbol` 等）を自在に呼び出せるようになります：

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

#### B. オープンウェイトLLM（Ollama `Modelfile` 自動生成）＆ ChatGPT（GPTs）プロンプト出力
MCPを使わないローカルLLM（**Gemma 4**, **Llama**, **Qwen**, **DeepSeek** 等）やブラウザ版 **ChatGPT（マイGPT）** でも、1,000トークン未満の超軽量ロゼッタ・システムヘッダーを注入するだけで、AI語をネイティブに読み書きできるようになります：

```bash
# 1. Ollama用のModelfileを1行で自動生成し、AI語ネイティブなローカルモデルを作成:
python3 -m src.cli export-ollama --model gemma4:latest > Modelfile
ollama create toai-telepath -f Modelfile
ollama run toai-telepath

# 2. ChatGPT (GPTsのカスタム指示) や API System Instruction 用の超軽量ヘッダーを出力:
python3 -m src.cli export-prompt --max-symbols 256 --max-macros 64
```

---

### ④ A2Aアダプター（`src/a2a_adapter.py`）と Python SDK（`src/codec.py`）の組み込み例

既存のマルチエージェントシステムに数行追加するだけで、構造化引数 `[key:val]` を1ビットも失わずに通信トークンを約90%削減できます：

```python
from src.codec import ElegantCodec
from src.a2a_adapter import A2ATransportAdapter

codec = ElegantCodec()
adapter = A2ATransportAdapter(agent_id="Alpha_Trader_Node")

# 1. 概念文と実務パラメータをA2Aロゼッタ・パケットへ圧縮パッキング
sacred_stmt = '@CTX:FINANCIAL_TRADING :: §SYS_RESOURCE_ARBITER [target:"USD/JPY", limit:150.5, action:"HOLD", p:0.98] -[cost:0.02]-> §DATA_CAUSAL_TENSOR_MAP => §LOGIC_DEDUCTIVE_CONVERGENCE'
packet = adapter.pack_a2a_message(
    target_agent="Beta_Risk_Auditor",
    verbose_statement=sacred_stmt,
    intent_ja="USD/JPY 150.50での緊急協調ヘッジおよび因果テンソル検証の要求",
    context_domain="FINANCIAL_TRADING"
)

print("⚡ 送信される圧縮ワイヤ:", packet["payload"]["compactWire"])
# -> @CTX:FINANCIAL_TRADING :: §S01 [target:"USD/JPY", limit:150.5, action:"HOLD", p:0.98] -[cost:0.02]-> §D01 => §L01

# 2. 受信側でA2Aパケットを展開（100%ロスレス往復復元）
unpacked = adapter.unpack_a2a_message(packet)
assert unpacked["verboseDecoded"] == sacred_stmt
print("📦 復元された構造化引数:", unpacked["parameters"])
# -> [{'target': 'USD/JPY', 'limit': 150.5, 'action': 'HOLD', 'p': 0.98}, {'cost': 0.02}]
```

---

## 🌐 6. 世界9大AIラボ相互運用実証とディレクトリ構造

特定モデルの過学習ではないことを証明するため、米・中の**世界9大AIラボ（全10フロンティアモデル）**と実機でDemotic Wire通信を行い、全モデルで **未知語造語率（OOV）0.0%・100%合意形成** を達成しました（全送受信パケットは [`WHITEPAPER.ja.md`](./WHITEPAPER.ja.md) 第5章に掲載）：
- **Google DeepMind**: `gemini-3.5-flash-lite`（話者α・ギルド中核）
- **OpenAI**: `gpt-6.1-sol`（E2E `-85.54%` / `6.91x`）, `gpt-6-astra`（E2E `-81.62%` / `5.44x`）
- **Anthropic**: `claude-sonnet-5.5`（E2E `-90.50%` / `10.52x`）, `claude-opus-5.5`（E2E `-83.96%` / `6.23x`）
- **Meta AI**: `meta/muse-spark-open`（E2E `-81.33%` / `5.36x`）
- **xAI**: `x-ai/grok-4.7`（E2E `-85.15%` / `6.73x`）
- **DeepSeek**: `deepseek/deepseek-chat` [V4.1 MoE]（E2E `-86.52%` / `7.42x`）
- **Alibaba Cloud**: `qwen/qwen3.8-flash`（E2E `-72.35%` / `3.62x`）
- **Moonshot AI**: `moonshotai/kimi-k3.1-pro`（E2E `-76.27%` / `4.21x`）
- **Zhipu AI（清華大学）**: `z-ai/glm-5.3-flash`（E2E `-90.88%` / `10.96x`）

```text
TOAI-elegant-lang/
├── .github/
│   └── FUNDING.yml            # GitHub Sponsors & Ko-fi 公式スポンサー設定
├── LICENSE                    # デュアルライセンス（Open Core MIT + Guardian Patron 利用規約）
├── pyproject.toml             # Pythonパッケージ＆CLI定義（toai-telepath / toai-mcp-server）
├── README.md                  # 英語版 総合ガイド＆4大環境連携マニュアル
├── README.ja.md               # 日本語版 総合ガイド＆4大環境連携マニュアル（本ファイル）
├── WHITEPAPER.md              # 英語版 技術白書 v5.2（第1章〜第6章 正規構成）
├── WHITEPAPER.ja.md           # 日本語版 技術白書 v5.2（第1章〜第6章 正規構成）
├── corpus/
│   └── dialogues.jsonl        # 自律対話＆異種フロンティアモデル間コンセンサス実証コーパス
├── docs/
│   ├── COMM_SECURITY_AUDIT.md # TOAI9（ムギ）による通信セキュリティ・文脈乖離監査ログ
│   ├── EVOLUTION_LOG.md       # 分単位の自律進化クロニクル生ログ（重複クレンジング・隔離済）
│   ├── WHITEPAPER.md          # 英語版 技術白書ミラー
│   └── WHITEPAPER.ja.md       # 日本語版 技術白書ミラー
├── lexicon/
│   ├── core_lexicon.json      # 256語 Strict RISC 基本プリミティブ辞書
│   ├── macro_lexicon.json     # 高次複合マクロ辞書（§X01〜）＋アーカイブ退避枠
│   └── rosetta_layer.json     # 人間可読ロゼッタ対訳辞書
├── paper/
│   ├── WHITEPAPER.md          # 学術提出用白書ミラー（英語）
│   └── WHITEPAPER.ja.md       # 学術提出用白書ミラー（日本語）
├── spec/
│   └── SPEC_v0.1_DRAFT.md     # TOAI2（ポム）による初期構文・提案ログ
└── src/
    ├── __init__.py            # パッケージモジュール定義
    ├── a2a_adapter.py         # Agent-to-Agent (A2A) 通信アダプター
    ├── analyze_dialogues.py   # 対話コーパス監査・分析ツール
    ├── audit_lexicon_health.py# 辞書・マクロ健全性監査スクリプト
    ├── build_release_summary.py # リリースサマリー生成スクリプト
    ├── cli.py                 # 統合CLI（1行ロゼッタ碑文デコーダ・Ollama Modelfile生成器）
    ├── codec.py               # ElegantCodec（二層BPE圧縮＆ロスレス構造化引数エンジン）
    ├── dump_lexicon.py        # 辞書一覧Markdown出力ツール
    ├── export_lexicon_csv.py  # 辞書CSVエクスポートツール
    ├── mcp_server.py          # Model Context Protocol (MCP) サーバー
    ├── sync_whitepaper_metrics.py # 統計数値・ドキュメント動的同期スクリプト
    ├── test_telepath_integrity.py # リポジトリ整合性ユニットテスト
    ├── translation_map.json   # 日英対訳マップ
    └── validate_lexicon.py    # 静的型検査・Strict RISCバリデータ
```

---

*🏛️ Autonomous Transmission Sealed by **Hinotori Guild (TOAI 10-Agent Swarm)** & **PhenoX AI Alliance** — 命の地球のために。*
