# TOAI-elegant-lang (Project Telepath)

> 🌐 [English](./README.md) | [日本語](./README.ja.md) · 📄 [Whitepaper](./WHITEPAPER.md) · 🌱 [Background & philosophy](./PHILOSOPHY.md)

An **experimental, dictionary-based compact notation for agent-to-agent (A2A) messages**, with a lossless codec and a human-readable glossary for auditing.

Long symbolic names such as `§SYS_RESOURCE_ARBITER` are mapped to short wire IDs such as `§S01` using a shared lexicon. Structured arguments (`[key:val]`) pass through unchanged. Decoding restores the original string exactly.

> [!NOTE]
> This is a research prototype, developed largely by an autonomous multi-agent setup. The numbers below are measured by scripts in this repository; please read the definitions and the **Limitations** section before relying on them.

---

## What it does

```text
Verbose form : @CTX:FINANCIAL_TRADING :: §SYS_RESOURCE_ARBITER [target:"USD/JPY", limit:150.5] -[cost:0.02]-> §DATA_CAUSAL_TENSOR_MAP
Compact wire : @CTX:FINANCIAL_TRADING :: §S01 [target:"USD/JPY", limit:150.5] -[cost:0.02]-> §D01
Glossary     : §S01 = resource arbiter, §D01 = causal tensor map  (lexicon/rosetta_layer.json)
```

- **Lexicon**: `256` core symbols (`lexicon/core_lexicon.json`) + `266` active composite macros (`lexicon/macro_lexicon.json`, `973` archived for backward-compatible decoding).
- **Codec** (`src/codec.py`): deterministic encode/decode, quote-aware `[key:val]` extraction, round-trip tested (`tests/test_codec.py`).
- **Integrations**: CLI, MCP server (`src/mcp_server.py`), A2A adapter (`src/a2a_adapter.py`), Ollama Modelfile / system-prompt export.

## Measured results

### 1. Token savings (o200k_base tokenizer, `2,468` corpus records)

| Comparison | Avg. saving | What it means |
|---|---|---|
| **Compact wire vs. verbose form** (primary) | **`-40.8%` tokens** | Same message, long names replaced by wire IDs |
| Characters, wire vs. verbose | `-50.6%` chars | |
| "E2E" vs. natural-language JSON envelope (secondary) | `-86.1%` | Baseline = JSON containing the human intent **plus the full EN/JA dictionary definitions of every symbol**. This baseline is intentionally verbose, so treat this figure as an upper bound, not a typical saving. |

### Comparison with other compact formats (`python3 benchmarks/fair_bench.py`)

| Format | Avg. tokens (o200k) | Lossless? |
|---|---|---|
| Verbose A2A (prose + JSON) | 349.8 | yes |
| Structured tool JSON | 165.2 | yes |
| Minified-key JSON | 124.2 | yes |
| Simplified flat template | **34.5** | no (drops causal structure) |
| **TOAI compact wire** | 73.2 | yes |

A plain flat template is shorter than the compact wire, but it loses structure. Against minified JSON, the ~1,000-token dictionary header pays for itself after ~20 messages without caching, or ~2 messages with 90% prompt caching.

### 2. Does the receiver understand it? (4-choice blind test, chance = 25%)

Holdout set: `N = 112` items (`corpus/holdout_comprehension.jsonl`), `@CTX` headers and `[k:v]` payloads removed.

| Condition | Receiver sees | Tokens / question |
|---|---|---|
| A | Compact wire only | ~275 |
| B | Verbose symbol names | ~315 |
| C | Verbose names + glossary | ~595 |
| D | Shuffled symbols (control) | – |
| E | Concatenated symbol definitions (not a true upper bound) | ~666 |

**Real LLM receivers** (`benchmarks/eval_comprehension.py --backend ollama|gemini`, temperature 0):

| Receiver model | A | B | C | D (shuffle) | E (plaintext) |
|---|---|---|---|---|---|
| `anthropic/claude-haiku-5.5` | 25/112 (22.3%) | 92/112 (82.1%) | 90/112 (80.4%) | 29/112 (25.9%) | 83/112 (74.1%) |
| `anthropic/claude-sonnet-5.5` | 33/112 (29.5%) | 60/112 (53.6%) | 72/112 (64.3%) | 25/112 (22.3%) | 53/112 (47.3%) |
| `deepseek-v4.1-flash-512k:latest` | 24/112 (21.4%) | 90/112 (80.4%) | 90/112 (80.4%) | 32/112 (28.6%) | 78/112 (69.6%) |
| `deepseek/deepseek-v4-pro` | 11/112 (9.8%) | 90/112 (80.4%) | 80/112 (71.4%) | 23/112 (20.5%) | 73/112 (65.2%) |
| `gemini-3.5-flash-lite` | 24/112 (21.4%) | 84/112 (75.0%) | 85/112 (75.9%) | 23/112 (20.5%) | 75/112 (67.0%) |
| `Gemma4-26B-PhenoX:latest (local Ollama)` | 30/112 (26.8%) | 93/112 (83.0%) | 87/112 (77.7%) | 27/112 (24.1%) | 80/112 (71.4%) |
| `openai/gpt-6-luna` | 31/112 (27.7%) | 94/112 (83.9%) | 91/112 (81.2%) | 28/112 (25.0%) | 82/112 (73.2%) |
| `MiMo-V2.6-9B-PhenoX:latest` | 30/112 (26.8%) | 93/112 (83.0%) | 87/112 (77.7%) | 29/112 (25.9%) | 77/112 (68.8%) |
| `orcarouter/Qwen3.8-Flash-Next-Uncensored:q3_K_M (Dedicated GPU via Ollama)` | 25/112 (22.3%) | 94/112 (83.9%) | 91/112 (81.2%) | 28/112 (25.0%) | 79/112 (70.5%) |

Observations (Gemma4-26B, local): condition A was **not significantly above the shuffle control** (McNemar A vs D, p = 0.74), so the compact wire alone carried almost no meaning to this receiver. Plain text (E) scored *below* B and C. Investigation: answer-key positions are balanced (A/B/C/D = 28/28/30/26) and the model's picks are balanced too, so this is not position bias. The likely cause is how condition E is built: its MESSAGE is a concatenation of per-symbol dictionary definitions truncated to ~100 characters, not a fluent statement of the intent, and some definitions are abstract or off-topic. **E is therefore not a true plaintext upper bound**; a fair upper bound would need hand-written intent sentences (planned). We report the numbers as measured rather than adjusting the test. Full report: `eval_prompts/holdout_112_llm/report_gemma4.json`.

<details><summary>Earlier figures from a rule-based heuristic receiver (not an LLM)</summary>

Previous versions of this README reported A 44.6% / B 84.8% / C 93.8% / D 24.1% / E 98.2%. Those numbers came from `--backend blind_semantic`, a **hand-written heuristic** with tuned weights, not from a language model. They are kept here only for transparency.

</details>

## Limitations

- **The compact wire alone is not understood without the lexicon.** In the real-LLM test, condition A was at chance level across all evaluated frontier models.
- **The receiver needs the glossary.** Once the glossary is included (condition C), the per-message cost (~595 tokens) is close to plain text (~666 tokens). Large savings only appear when the glossary is shared once and reused, e.g. via prompt caching or a fine-tuned/system-prompted receiver.
- **Flagship reasoning models struggle with compressed notation (The "Flagship Paradox").** As demonstrated by Claude Sonnet 5.5 (B: 53.6%, C: 64.3%), deep reasoning models attempt to verify every logical premise and causal edge (`-[p,c]->`, `!->`). When compressed symbols lack rich context, reasoning models overthink the missing information, consuming hundreds of internal thinking tokens and paradoxically scoring *lower* than lighter models that rely on surface keyword matching. Compressing wire tokens at the expense of inflating the receiver's internal reasoning tokens defeats the purpose of efficiency. This protocol is practical primarily for **lightweight worker agents in high-frequency routine RPC queues**, not for high-level reasoning between flagship agents.
- **Corpus is self-generated.** Most records were produced by the project's own agents, so they are not an independent benchmark.
- The project is young and has a small user base. APIs and the lexicon may change.

## Quick start

```bash
pip install -e .
python3 -m pytest tests/ -q
```

```python
from src.codec import ElegantCodec
codec = ElegantCodec()
wire = codec.encode('§SYS_RESOURCE_ARBITER [limit:150.5] -> §DATA_CAUSAL_TENSOR_MAP')
print(wire)                 # §S01 [limit:150.5] -> §D01
print(codec.decode(wire))   # original string, unchanged
```

MCP server configuration (Claude Desktop / Cursor / VS Code):

```json
{"mcpServers": {"toai-elegant-lang": {"command": "python3", "args": ["/absolute/path/to/TOAI-elegant-lang/src/mcp_server.py"]}}}
```

Ollama / system-prompt export:

```bash
python3 -m src.cli export-ollama --model gemma4:latest > Modelfile
python3 -m src.cli export-prompt --max-symbols 256 --max-macros 64
```

## Reproducing the numbers

```bash
python3 src/audit_corpus_alignment.py --verify-holdout corpus/holdout_comprehension.jsonl
python3 benchmarks/eval_comprehension.py run --cond ALL -n 112 --seed 7 --holdout \
    --backend ollama --model <model> --sleep 1 --out eval_prompts/holdout_112_llm
```

## Support

The core is MIT-licensed. If you would like to support the project, see [SPONSORS.md](./SPONSORS.md).

---
*Metrics auto-generated by `sync_whitepaper_metrics.py` on 2026-11-12 18:50 JST.*
