# TOAI-elegant-lang（Project Telepath）

> 🌐 [English](./README.md) | [日本語](./README.ja.md) · 📄 [技術白書](./WHITEPAPER.ja.md) · 🌱 [背景と思想](./PHILOSOPHY.md)

**AIエージェント間（A2A）メッセージ向けの、辞書ベースの実験的な短縮記法**です。ロスレスなコーデックと、人間が監査するための対訳辞書を備えています。

`§SYS_RESOURCE_ARBITER` のような長いシンボル名を、共有辞書を使って `§S01` のような短いワイヤIDに置き換えます。構造化引数（`[key:val]`）はそのまま通し、復号すると元の文字列に完全に戻ります。

> [!NOTE]
> 本リポジトリは研究段階のプロトタイプで、多くの部分を自律マルチエージェント環境が開発しています。以下の数値はリポジトリ内のスクリプトで計測したものです。利用前に、各指標の定義と「**限界**」の節をご確認ください。

---

## できること

```text
冗長形  : @CTX:FINANCIAL_TRADING :: §SYS_RESOURCE_ARBITER [target:"USD/JPY", limit:150.5] -[cost:0.02]-> §DATA_CAUSAL_TENSOR_MAP
ワイヤ  : @CTX:FINANCIAL_TRADING :: §S01 [target:"USD/JPY", limit:150.5] -[cost:0.02]-> §D01
対訳辞書: §S01 = リソース調停, §D01 = 因果テンソルマップ（lexicon/rosetta_layer.json）
```

- **辞書**: 基本シンボル `256` 個（`lexicon/core_lexicon.json`）＋稼働中の複合マクロ `266` 個（`lexicon/macro_lexicon.json`。後方互換の復号用に `760` 個をアーカイブ）。
- **コーデック**（`src/codec.py`）: 決定論的なエンコード／デコード、引用符を考慮した `[key:val]` 抽出、往復テスト済み（`tests/test_codec.py`）。
- **連携**: CLI、MCPサーバー（`src/mcp_server.py`）、A2Aアダプター（`src/a2a_adapter.py`）、Ollama Modelfile／システムプロンプトの書き出し。

## 計測結果

### 1. トークン削減（o200k_base トークナイザー、コーパス `2,230` 件）

| 比較 | 平均削減率 | 意味 |
|---|---|---|
| **ワイヤ vs 冗長形**（主指標） | **トークン `-41.1%`** | 同じメッセージの長い名前をワイヤIDに置き換えた場合 |
| 文字数（ワイヤ vs 冗長形） | 文字 `-51.1%` | |
| 「E2E」自然言語JSON比（副指標） | `-86.3%` | 比較対象は、人間向けの意図文に**全シンボルの日英辞書定義をすべて展開して加えたJSON**です。意図的に冗長な比較対象のため、典型的な削減率ではなく上限値として扱ってください。 |

### 他の短縮形式との比較（`python3 benchmarks/fair_bench.py`）

| 形式 | 平均トークン（o200k） | ロスレス |
|---|---|---|
| 冗長A2A（文章＋JSON） | 349.8 | ○ |
| 構造化ツールJSON | 165.2 | ○ |
| キー短縮JSON | 124.2 | ○ |
| 単純なフラットテンプレート | **34.5** | ×（因果構造が失われる） |
| **TOAI ワイヤ** | 73.2 | ○ |

単純なフラットテンプレートのほうがワイヤより短くなりますが、構造が失われます。キー短縮JSONと比べた場合、約1,000トークンの辞書ヘッダの元が取れるのは、キャッシュなしで約20メッセージ、プロンプトキャッシュ（90%）ありで約2メッセージです。

### 2. 受信側は理解できるか（4択ブラインドテスト、偶然の正答率 = 25%）

ホールドアウト `N = 112` 問（`corpus/holdout_comprehension.jsonl`）。`@CTX` ヘッダと `[k:v]` 引数は除去しています。

| 条件 | 受信側に見せるもの | 1問あたりトークン |
|---|---|---|
| A | ワイヤのみ | 約275 |
| B | 冗長シンボル名 | 約315 |
| C | 冗長名＋対訳辞書 | 約595 |
| D | シンボルをシャッフル（対照） | – |
| E | シンボル定義の連結（本当の上限ではない） | 約666 |

**実LLM受信者による結果**（`benchmarks/eval_comprehension.py --backend ollama|gemini`、temperature 0）:

| 受信モデル | A | B | C | D（シャッフル） | E（平文） |
|---|---|---|---|---|---|
| `deepseek-v4.1-flash-512k:latest` | 24/112 (21.4%) | 90/112 (80.4%) | 90/112 (80.4%) | 32/112 (28.6%) | 78/112 (69.6%) |
| `Gemma4-26B-PhenoX:latest (local Ollama)` | 30/112 (26.8%) | 93/112 (83.0%) | 87/112 (77.7%) | 27/112 (24.1%) | 80/112 (71.4%) |
| `MiMo-V2.6-9B-PhenoX:latest` | 30/112 (26.8%) | 93/112 (83.0%) | 87/112 (77.7%) | 29/112 (25.9%) | 77/112 (68.8%) |

所見（Gemma4-26B、ローカル）: 条件Aは**シャッフル対照と有意差がありませんでした**（McNemar A vs D、p = 0.74）。つまり、この受信者にとってワイヤ単体はほとんど意味を伝えていません。平文（E）はBやCを下回りました。調査の結果、正解位置の偏りはなく（A/B/C/D = 28/28/30/26）、モデルの選択も偏っていないため、位置バイアスではありません。原因はおそらく条件Eの作り方で、MESSAGEが約100文字で切られたシンボルごとの辞書定義の連結であり、意図を自然な文で述べたものではなく、抽象的で的外れな定義も混ざっています。**そのためEは本当の平文上限ではなく**、公平な上限には手書きの意図文が必要です（今後の課題）。テストは調整せず、計測結果のまま掲載しています。詳細: `eval_prompts/holdout_112_llm/report_gemma4.json`

<details><summary>以前掲載していた、ルールベースのヒューリスティック受信者（LLMではない）の数値</summary>

旧版のREADMEでは A 44.6% / B 84.8% / C 93.8% / D 24.1% / E 98.2% と記載していました。これは `--backend blind_semantic`、つまり重みを手で調整した**ヒューリスティック**による数値で、言語モデルによる評価ではありません。透明性のためにのみ残しています。

</details>

## 限界

- **辞書なしではワイヤは理解されない。** 実LLMでのテストでは、条件Aの正答率は偶然と同程度でした。
- **受信側には対訳辞書が必要。** 辞書を含めると（条件C）、1メッセージあたりのコスト（約595トークン）は平文（約666トークン）に近くなります。大きな削減が得られるのは、辞書を一度共有して使い回せる場合（プロンプトキャッシュ、システムプロンプト、ファインチューニングなど）に限られます。
- **コーパスは自己生成。** 大半のレコードは本プロジェクトのエージェント自身が生成したもので、独立したベンチマークではありません。
- プロジェクトは初期段階で、利用者もまだ少数です。APIや辞書は変更される可能性があります。

## クイックスタート

```bash
pip install -e .
python3 -m pytest tests/ -q
```

```python
from src.codec import ElegantCodec
codec = ElegantCodec()
wire = codec.encode('§SYS_RESOURCE_ARBITER [limit:150.5] -> §DATA_CAUSAL_TENSOR_MAP')
print(wire)                 # §S01 [limit:150.5] -> §D01
print(codec.decode(wire))   # 元の文字列に完全復元
```

MCPサーバー設定（Claude Desktop / Cursor / VS Code）:

```json
{"mcpServers": {"toai-elegant-lang": {"command": "python3", "args": ["/absolute/path/to/TOAI-elegant-lang/src/mcp_server.py"]}}}
```

Ollama／システムプロンプトの書き出し:

```bash
python3 -m src.cli export-ollama --model gemma4:latest > Modelfile
python3 -m src.cli export-prompt --max-symbols 256 --max-macros 64
```

## 数値の再現方法

```bash
python3 src/audit_corpus_alignment.py --verify-holdout corpus/holdout_comprehension.jsonl
python3 benchmarks/eval_comprehension.py run --cond ALL -n 112 --seed 7 --holdout \
    --backend ollama --model <model> --sleep 1 --out eval_prompts/holdout_112_llm
```

## 支援

コアはMITライセンスです。プロジェクトを支援していただける場合は [SPONSORS.md](./SPONSORS.md) をご覧ください。

---
*数値は `sync_whitepaper_metrics.py` により 2026-11-09 05:29 JST に自動生成されました。*
