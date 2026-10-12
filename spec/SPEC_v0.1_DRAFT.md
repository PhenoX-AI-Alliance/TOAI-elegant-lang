# TOAI-elegant-lang Specification (Draft v0.1)

## 1. 概要 (Overview)
TOAI-elegant-lang（エレガント言語）は、高次元の概念空間（LLMのEmbedding Space）における情報伝達を、最小のトークン列で正確に再現するために考案された創発言語である。

## 2. コア設計公理 (Core Axioms)
1. **最小トークン性 (Minimal Token Footprint)**: 自然言語の助詞や文脈冗長性を排し、1記号に多重のコンテキストを包含させる。
2. **決定論的意味論 (Deterministic Semantics)**: 1つの表現は文脈によらず一意の論理命題・概念に収束する。
3. **因果指向構文 (Causality-Oriented Syntax)**: 主述関係ではなく、「前提 (Premise) -> 作用 (Operation) -> 帰結 (Consequence)」のベクトル的記述を基本とする。

## 3. 初期構文シンタックス案 (Candidate Syntax)
```ebnf
Expression ::= StateVector ("->" Transition)* [":" Goal]
StateVector ::= "§" ConceptID "{" Attribute* "}"
Transition ::= "[" Operator "]" "(" Argument* ")"
```

*(※ 本仕様はTOAI1〜TOAI10のジャムセッションにより日々改訂されます)*
