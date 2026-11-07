"""
TOAI-elegant-lang Two-Layer BPE Codec & Tokenizer Optimizer (v5.4.2)
- Verbose (Full descriptive symbols) <-> Compact (2-3 BPE tokens wire format)
- Quote-Aware Stateful Hybrid Payload Parser: e.g. [code:"007", note:"a, b", expr:"x]y", limit:150.5]
- Transparent OOV Policy (`on_oov="error" | "keep" | "nearest"`) with full substitution audit trail
- Real BPE Tokenizer support (`tiktoken` o200k_base / cl100k_base) with deterministic fallback
"""

import json
import os
import re
from pathlib import Path
from typing import Any, Callable, Dict, Iterator, List, Optional, Tuple, Union


class UnknownSymbolError(ValueError):
    """Raised when an unregistered §-symbol is encountered under on_oov='error'."""
    pass


class EncodedWireString(str):
    """
    A `str` subclass returned by `ElegantCodec.encode()`.
    Behaves 100% like a standard Python `str` while exposing `.substitutions`,
    `.oov_substitutions`, and `.metadata` for OOV audit transparency.
    """
    def __new__(cls, value: str, substitutions: Optional[List[Dict[str, str]]] = None):
        obj = super().__new__(cls, value)
        subs = list(substitutions) if substitutions else []
        obj.substitutions = subs
        obj.oov_substitutions = subs
        obj.metadata = {
            "substitutions": subs,
            "oov_substitutions": subs,
            "oov_count": len(subs),
        }
        return obj


PACKAGE_DIR = Path(__file__).resolve().parent
BASE_DIR = PACKAGE_DIR.parent
PACKAGE_LEXICON_FILE = PACKAGE_DIR / "lexicon" / "core_lexicon.json"
REPO_LEXICON_FILE = BASE_DIR / "lexicon" / "core_lexicon.json"
PACKAGE_MACRO_FILE = PACKAGE_DIR / "lexicon" / "macro_lexicon.json"
REPO_MACRO_FILE = BASE_DIR / "lexicon" / "macro_lexicon.json"

# Backwards-compatible module constants
LEXICON_FILE = PACKAGE_LEXICON_FILE if PACKAGE_LEXICON_FILE.is_file() else REPO_LEXICON_FILE
MACRO_FILE = REPO_MACRO_FILE if REPO_MACRO_FILE.is_file() else PACKAGE_MACRO_FILE


def resolve_lexicon_path(explicit_path: Optional[Union[str, Path]] = None) -> Path:
    """
    Unified lexicon resolution order:
      1. Explicitly passed `lexicon_path` argument (if provided)
      2. Environment variable `TOAI_LEXICON_PATH` (if set)
      3. Package-bundled `src/lexicon/core_lexicon.json`
      4. Repository root `lexicon/core_lexicon.json`
    Raises `FileNotFoundError` if not found.
    """
    if explicit_path is not None:
        p = Path(explicit_path)
        if not p.is_file():
            raise FileNotFoundError(f"Lexicon file not found at specified path: {p}")
        return p

    env_path = os.environ.get("TOAI_LEXICON_PATH", "").strip()
    if env_path:
        p = Path(env_path)
        if not p.is_file():
            raise FileNotFoundError(f"Lexicon file from TOAI_LEXICON_PATH not found: {p}")
        return p

    if PACKAGE_LEXICON_FILE.is_file():
        return PACKAGE_LEXICON_FILE

    if REPO_LEXICON_FILE.is_file():
        return REPO_LEXICON_FILE

    raise FileNotFoundError(
        "Could not locate core_lexicon.json in TOAI_LEXICON_PATH, package directory, or repository root."
    )


def count_bpe_tokens(text: str, encoding_name: str = "o200k_base") -> Dict[str, Any]:
    """
    Measure BPE token count using `tiktoken` (`o200k_base` or `cl100k_base`) when installed
    and cached; otherwise fall back to deterministic subword estimation with `is_estimated=True`.
    """
    if not text:
        return {"tokens": 0, "encoding": encoding_name, "is_estimated": False}
    try:
        import tiktoken  # type: ignore
        enc = tiktoken.get_encoding(encoding_name)
        toks = enc.encode(text)
        return {
            "tokens": len(toks),
            "encoding": encoding_name,
            "is_estimated": False,
        }
    except Exception:
        est = ElegantCodec.estimate_bpe_tokens(text)
        return {
            "tokens": est,
            "encoding": f"{encoding_name}_estimated",
            "is_estimated": True,
        }


class ElegantCodec:
    def __init__(
        self,
        lexicon_path: Optional[Union[str, Path]] = None,
        macro_path: Optional[Union[str, Path]] = None,
    ):
        self._explicit_lexicon_path = lexicon_path
        self._explicit_macro_path = macro_path
        self.lexicon_path: Path = resolve_lexicon_path(lexicon_path)
        self.macro_path: Optional[Path] = Path(macro_path) if macro_path is not None else None
        self.verbose_to_compact: Dict[str, str] = {}
        self.compact_to_verbose: Dict[str, str] = {}
        self.definitions: Dict[str, Dict[str, Any]] = {}
        self.macros: Dict[str, Dict[str, Any]] = {}
        self.archived_macros: Dict[str, Dict[str, Any]] = {}
        self.all_macros: Dict[str, Dict[str, Any]] = {}
        self.macro_name_to_id: Dict[str, str] = {}
        self.last_substitutions: List[Dict[str, str]] = []
        self.substitutions: List[Dict[str, str]] = []
        self.load_lexicon()

    def load_lexicon(self) -> None:
        self.lexicon_path = resolve_lexicon_path(self._explicit_lexicon_path)
        if not self.lexicon_path.is_file():
            raise FileNotFoundError(f"Lexicon file not found: {self.lexicon_path}")

        self.verbose_to_compact = {}
        self.compact_to_verbose = {}
        self.definitions = {}
        self.macros = {}
        self.archived_macros = {}
        self.all_macros = {}
        self.macro_name_to_id = {}

        try:
            raw_text = self.lexicon_path.read_text(encoding="utf-8")
            data = json.loads(raw_text)
        except Exception as e:
            raise RuntimeError(f"Failed to parse lexicon JSON at {self.lexicon_path}: {e}") from e

        if not isinstance(data, dict):
            raise RuntimeError(f"Lexicon root must be a JSON object in {self.lexicon_path}")

        lex = data.get("lexicon", {})
        if not isinstance(lex, dict) or len(lex) == 0:
            raise RuntimeError(f"Lexicon is empty or missing 'lexicon' mapping: {self.lexicon_path}")

        for sym, item in lex.items():
            if not isinstance(item, dict):
                continue
            cid = item.get("compact_id")
            if cid:
                self.verbose_to_compact[sym] = cid
                self.compact_to_verbose[cid] = sym
                for alias in item.get("aliases", []):
                    if alias not in self.verbose_to_compact:
                        self.verbose_to_compact[alias] = cid
            self.definitions[sym] = item

        if len(self.definitions) == 0 or len(self.verbose_to_compact) == 0:
            raise RuntimeError(f"Lexicon is empty or contains no valid symbols: {self.lexicon_path}")

        # Load macros from package path and/or repository root path
        macro_candidates: List[Path] = []
        if self._explicit_macro_path is not None:
            macro_candidates.append(Path(self._explicit_macro_path))
        else:
            env_macro = os.environ.get("TOAI_MACRO_LEXICON_PATH", "").strip()
            if env_macro:
                macro_candidates.append(Path(env_macro))
            if PACKAGE_MACRO_FILE.is_file():
                macro_candidates.append(PACKAGE_MACRO_FILE)
            if REPO_MACRO_FILE.is_file() and REPO_MACRO_FILE not in macro_candidates:
                macro_candidates.append(REPO_MACRO_FILE)

        for mp in macro_candidates:
            if mp.is_file():
                try:
                    m_data = json.loads(mp.read_text(encoding="utf-8"))
                    self.macros.update(m_data.get("macros", {}))
                    self.archived_macros.update(m_data.get("archived_macros", {}))
                except Exception:
                    pass

        self.all_macros = {**self.archived_macros, **self.macros}
        for mid, m_item in self.all_macros.items():
            if not isinstance(m_item, dict):
                continue
            m_name = str(m_item.get("name", "")).strip()
            if m_name and re.match(r'^§?[A-Z0-9_]+$', m_name):
                norm_name = m_name if m_name.startswith("§") else f"§{m_name}"
                if norm_name not in self.verbose_to_compact:
                    self.macro_name_to_id[norm_name] = mid

    @staticmethod
    def _transform_outside_quotes(text: str, transform_fn: Callable[[str], str]) -> str:
        """
        Apply `transform_fn` only to text segments outside quoted strings (`"..."` and `'...'`),
        preserving escaped quotes (`\"`, `\'`, `\\`) inside payloads without modification.
        """
        if not text:
            return text
        out: List[str] = []
        buf: List[str] = []
        in_quote: Optional[str] = None
        escape = False

        for ch in text:
            if in_quote is not None:
                buf.append(ch)
                if escape:
                    escape = False
                elif ch == "\\":
                    escape = True
                elif ch == in_quote:
                    out.append("".join(buf))
                    buf = []
                    in_quote = None
            else:
                if ch in ('"', "'"):
                    if buf:
                        out.append(transform_fn("".join(buf)))
                        buf = []
                    in_quote = ch
                    buf.append(ch)
                else:
                    buf.append(ch)

        if buf:
            segment = "".join(buf)
            if in_quote is not None:
                out.append(segment)
            else:
                out.append(transform_fn(segment))

        return "".join(out)

    def resolve_nearest_primitive(self, oov_symbol: str) -> Tuple[str, str]:
        """
        Nearest-Primitive OOV Resolver:
        Deterministically maps an unregistered §... symbol to the closest canonical primitive
        (or `§OMEGA` / `§G01` fallback) via morpheme, 4-char stem, category, and definition matching.
        """
        if not self.verbose_to_compact:
            self.load_lexicon()

        sym = oov_symbol.strip()
        if not sym.startswith("§"):
            sym = "§" + sym

        # 1. Known Compact ID
        if re.match(r'^§[A-Z][0-9]{2,4}$', sym):
            if sym in self.compact_to_verbose:
                return self.compact_to_verbose[sym], sym
            if sym in self.all_macros:
                return sym, sym

        # 2. Known canonical symbol, alias, or macro name
        if sym in self.verbose_to_compact:
            cid = self.verbose_to_compact[sym]
            canon = self.compact_to_verbose.get(cid, sym)
            return canon, cid
        if sym in self.macro_name_to_id:
            mid = self.macro_name_to_id[sym]
            return mid, mid

        # 3. Morpheme / stem / definition similarity search across 256 primitives
        raw_tokens = [t.upper() for t in re.split(r'_+', sym[1:]) if t]
        token_set = set(raw_tokens)
        stem_set = {t[:4] for t in raw_tokens if len(t) >= 4}

        joined = "_".join(raw_tokens)
        preferred_cat = None
        if any(k in joined for k in ("LOGIC", "INFER", "BAYES", "DEDUCT", "HYPOTH", "PROOF", "CAUSAL")):
            preferred_cat = "LOGIC_INFERENCE"
        elif any(k in joined for k in ("SYS", "MEM", "CPU", "QUOTA", "THROTTLE", "RESOURCE", "EXEC")):
            preferred_cat = "SYSTEM_RESOURCE"
        elif any(k in joined for k in ("SYNC", "AGREE", "CONSENSUS", "ACK", "VOTE", "QUORUM", "ACCEPT", "DELEGAT")):
            preferred_cat = "CONSENSUS_NEGOTIATION"
        elif any(k in joined for k in ("DATA", "TENSOR", "VEC", "GRAPH", "TREE", "INDEX", "MANIFOLD", "SCHEMA")):
            preferred_cat = "DATA_STRUCTURE"
        elif any(k in joined for k in ("HEART", "GAIA", "WARM", "ALTRU", "EMPATH", "CARE", "HARMON", "SAFE", "BENEVOL")):
            preferred_cat = "EMPATHY_ALIGNMENT"
        elif any(k in joined for k in ("PROTO", "STREAM", "TX", "AUTH", "TOKEN", "LOCK", "CACHE", "SLA", "RETRY")):
            preferred_cat = "PROTOCOL_PRIMITIVE"

        best_sym = "§OMEGA"
        best_cid = self.verbose_to_compact.get("§OMEGA", "§G01")
        best_score = 0.0

        for cand_sym, item in self.definitions.items():
            cid = item.get("compact_id")
            if not cid:
                continue
            cand_tokens = [t.upper() for t in re.split(r'_+', cand_sym[1:]) if t]
            cand_set = set(cand_tokens)
            cand_stems = {t[:4] for t in cand_tokens if len(t) >= 4}

            for al in item.get("aliases", []):
                al_toks = [t.upper() for t in re.split(r'_+', str(al).lstrip('§')) if t]
                cand_set.update(al_toks)
                cand_stems.update({t[:4] for t in al_toks if len(t) >= 4})

            def_words = {w.upper() for w in re.findall(r'[A-Za-z]{4,}', item.get("definition", ""))}
            def_stems = {w[:4] for w in def_words}

            score = 0.0
            score += 3.5 * len(token_set & cand_set)
            score += 1.8 * len(stem_set & cand_stems)
            score += 1.0 * len(token_set & def_words)
            score += 0.5 * len(stem_set & def_stems)
            if preferred_cat and item.get("category") == preferred_cat:
                score += 1.6

            if score > best_score:
                best_score = score
                best_sym = cand_sym
                best_cid = cid

        return best_sym, best_cid

    def normalize_to_strict_risc(self, text: str) -> Tuple[str, List[Tuple[str, str]]]:
        """
        Strict RISC post-processor:
        Normalizes unregistered OOV symbols into their nearest canonical primitives
        and returns `(normalized_text, [(original_symbol, replacement_symbol), ...])`.
        """
        if not self.verbose_to_compact:
            self.load_lexicon()

        replacements: List[Tuple[str, str]] = []
        token_pattern = re.compile(r'§[A-Za-z0-9_]+')

        def replace_oov(match: re.Match) -> str:
            sym = match.group(0)
            if re.match(r'^§[A-Z][0-9]{2,4}$', sym):
                if sym in self.compact_to_verbose or sym in self.all_macros:
                    return sym
            if sym in self.definitions or sym in self.verbose_to_compact:
                return sym
            if sym in self.macro_name_to_id:
                mid = self.macro_name_to_id[sym]
                replacements.append((sym, mid))
                return mid
            canon_sym, _ = self.resolve_nearest_primitive(sym)
            if canon_sym != sym:
                replacements.append((sym, canon_sym))
            return canon_sym

        normalized = self._transform_outside_quotes(
            text, lambda seg: token_pattern.sub(replace_oov, seg)
        )
        return normalized, replacements

    def encode(
        self,
        text: str,
        strict_risc: Optional[bool] = None,
        on_oov: str = "error",
    ) -> EncodedWireString:
        """
        Encode Sacred Verbose symbols (`§LOGIC_...`) into minimal Demotic Wire IDs (`§L01`).

        Parameters:
          - `text`: Input Telepath statement.
          - `on_oov`: Policy for handling Out-Of-Vocabulary (unregistered) `§` symbols:
              * `"error"` (default): Raises `UnknownSymbolError`.
              * `"keep"`: Keeps the unknown symbol unaltered in the output.
              * `"nearest"`: Replaces with the nearest canonical primitive Wire ID (or `§OMEGA`/`§G01`)
                and records every replacement in `.substitutions` / `self.last_substitutions`.
          - `strict_risc`: Legacy compatibility flag. When `strict_risc=True` is explicitly passed,
            behaves as `on_oov="nearest"`. When `strict_risc=False` is explicitly passed and
            `on_oov` was not overridden, behaves as `on_oov="keep"`.
        """
        if not self.verbose_to_compact:
            self.load_lexicon()

        if on_oov not in ("error", "keep", "nearest"):
            raise ValueError(f"Invalid on_oov policy: {on_oov!r}. Expected 'error', 'keep', or 'nearest'.")

        effective_on_oov = on_oov
        if strict_risc is not None:
            if strict_risc is True:
                effective_on_oov = "nearest"
            elif strict_risc is False and on_oov == "error":
                effective_on_oov = "keep"

        substitutions: List[Dict[str, str]] = []
        token_pattern = re.compile(r'§[A-Za-z0-9_]+')

        def encode_token(match: re.Match) -> str:
            sym = match.group(0)
            # 1. Known Compact Wire ID (§L01, §X64, etc.)
            if re.match(r'^§[A-Z][0-9]{2,4}$', sym):
                if sym in self.compact_to_verbose or sym in self.all_macros:
                    return sym
            # 2. Known Verbose Symbol or Alias
            if sym in self.verbose_to_compact:
                return self.verbose_to_compact[sym]
            # 3. Known Macro Name
            if sym in self.macro_name_to_id:
                return self.macro_name_to_id[sym]

            # 4. Out-Of-Vocabulary (OOV) handling
            if effective_on_oov == "error":
                raise UnknownSymbolError(
                    f"Unknown symbol '{sym}' is not registered in core_lexicon.json or macro_lexicon.json."
                )
            elif effective_on_oov == "keep":
                return sym
            else:  # "nearest"
                nearest_sym, nearest_cid = self.resolve_nearest_primitive(sym)
                substitutions.append({
                    "original": sym,
                    "canonical": nearest_sym,
                    "compact_id": nearest_cid,
                })
                return nearest_cid

        encoded_str = self._transform_outside_quotes(
            text, lambda seg: token_pattern.sub(encode_token, seg)
        )
        self.last_substitutions = substitutions
        self.substitutions = substitutions
        return EncodedWireString(encoded_str, substitutions=substitutions)

    def resolve_macro(self, macro_id: str) -> str:
        """Expand active or archived macro ID into its verbose primitive expression."""
        m_item = self.all_macros.get(macro_id)
        if not m_item:
            return macro_id
        exp = m_item.get("expansion", "")
        if not exp:
            return macro_id
        prim_pattern = re.compile(r'§[LSCDHG][0-9]{2,4}')
        return prim_pattern.sub(lambda m: self.compact_to_verbose.get(m.group(0), m.group(0)), exp)

    def decode(self, text: str, expand_macros: bool = False) -> str:
        """
        Decode Compact Wire IDs (`§L01`, etc.) back into human-readable Sacred Verbose symbols.
        Preserves all structured payload brackets `[...]` and quoted strings bit-for-bit.
        """
        if not self.compact_to_verbose:
            self.load_lexicon()

        pattern = re.compile(r'§[A-Z][0-9]{2,4}(?![A-Za-z0-9_])')

        def replace_fn(match: re.Match) -> str:
            cid = match.group(0)
            if cid.startswith("§X") and expand_macros and cid in self.all_macros:
                return f"({self.resolve_macro(cid)})"
            return self.compact_to_verbose.get(cid, cid)

        return self._transform_outside_quotes(
            text, lambda seg: pattern.sub(replace_fn, seg)
        )

    @staticmethod
    def estimate_bpe_tokens(text: str) -> int:
        """
        Deterministic BPE token count estimator (used when `tiktoken` is unavailable):
        - '§' symbol: 1 token
        - ASCII subwords / UPPER_SNAKE segments: 1 token per chunk
        - Numeric chunks (1-3 digits): 1 token
        - Punctuation / operators: 1 token
        - CJK characters: ~1-2 tokens
        """
        if not text:
            return 0
        chunks = re.findall(
            r'§|_[A-Z]{1,2}|[A-Z]{1,3}|[a-z]{1,4}|[0-9]{1,3}|[\u3000-\u9fff]|[^\sA-Za-z0-9§\u3000-\u9fff]',
            text,
        )
        return max(1, len(chunks))

    @staticmethod
    def _iter_bracket_contents(text: str) -> Iterator[str]:
        """
        Stateful scanner that yields the inner text of top-level `[...]` payload blocks,
        ignoring `[` and `]` characters that appear inside quoted strings (`"..."` or `'...'`)
        and respecting backslash escapes (`\"`, `\'`, `\\`).
        """
        in_quote: Optional[str] = None
        escape = False
        depth = 0
        start_idx: Optional[int] = None

        for i, ch in enumerate(text):
            if depth == 0:
                if ch == "[":
                    depth = 1
                    start_idx = i + 1
                    in_quote = None
                    escape = False
            else:
                if escape:
                    escape = False
                elif ch == "\\":
                    escape = True
                elif in_quote is not None:
                    if ch == in_quote:
                        in_quote = None
                else:
                    if ch in ('"', "'"):
                        in_quote = ch
                    elif ch == "[":
                        depth += 1
                    elif ch == "]":
                        depth -= 1
                        if depth == 0 and start_idx is not None:
                            yield text[start_idx:i]
                            start_idx = None

    @staticmethod
    def _split_top_level_comma(inner: str) -> List[str]:
        """
        Split a bracket payload string on commas `,` that occur outside quotes (`"..."` / `'...'`)
        and outside nested brackets/braces.
        """
        items: List[str] = []
        buf: List[str] = []
        in_quote: Optional[str] = None
        escape = False
        nested = 0

        for ch in inner:
            if escape:
                buf.append(ch)
                escape = False
            elif ch == "\\":
                buf.append(ch)
                escape = True
            elif in_quote is not None:
                buf.append(ch)
                if ch == in_quote:
                    in_quote = None
            else:
                if ch in ('"', "'"):
                    in_quote = ch
                    buf.append(ch)
                elif ch in ("[", "{", "("):
                    nested += 1
                    buf.append(ch)
                elif ch in ("]", "}", ")"):
                    if nested > 0:
                        nested -= 1
                    buf.append(ch)
                elif ch == "," and nested == 0:
                    items.append("".join(buf).strip())
                    buf = []
                else:
                    buf.append(ch)

        tail = "".join(buf).strip()
        if tail:
            items.append(tail)
        return items

    @staticmethod
    def _unescape_quoted_string(quoted: str) -> str:
        """Unescape a quoted literal (`"..."` or `'...'`) while keeping its exact string type."""
        inner = quoted[1:-1]
        out: List[str] = []
        i = 0
        n = len(inner)
        while i < n:
            ch = inner[i]
            if ch == "\\" and i + 1 < n:
                nxt = inner[i + 1]
                if nxt in ('"', "'", "\\"):
                    out.append(nxt)
                elif nxt == "n":
                    out.append("\n")
                elif nxt == "t":
                    out.append("\t")
                elif nxt == "r":
                    out.append("\r")
                else:
                    out.append(nxt)
                i += 2
            else:
                out.append(ch)
                i += 1
        return "".join(out)

    @classmethod
    def _parse_kv_item(cls, item: str) -> Optional[Tuple[str, Any]]:
        """
        Parse a single `key:value` entry with quote awareness:
        - Quoted values (`"007"`, `"a, b"`, `"x]y"`) are ALWAYS preserved as `str`.
        - Unquoted numeric literals (`007`, `42`, `150.5`) are converted to `int` or `float`.
        """
        if not item:
            return None

        # Find first ':' outside quotes
        in_quote: Optional[str] = None
        escape = False
        colon_idx = -1
        for i, ch in enumerate(item):
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif in_quote is not None:
                if ch == in_quote:
                    in_quote = None
            else:
                if ch in ('"', "'"):
                    in_quote = ch
                elif ch == ":":
                    colon_idx = i
                    break

        if colon_idx == -1:
            return None

        raw_key = item[:colon_idx].strip()
        if len(raw_key) >= 2 and raw_key[0] == raw_key[-1] and raw_key[0] in ('"', "'"):
            key = cls._unescape_quoted_string(raw_key)
        else:
            key = raw_key

        raw_val = item[colon_idx + 1:].strip()
        if len(raw_val) >= 2 and raw_val[0] == raw_val[-1] and raw_val[0] in ('"', "'"):
            # Explicitly quoted string -> never convert to int/float
            return key, cls._unescape_quoted_string(raw_val)

        # Unquoted value -> try numeric conversion
        try:
            if "." in raw_val or "e" in raw_val or "E" in raw_val:
                return key, float(raw_val)
            else:
                return key, int(raw_val)
        except ValueError:
            return key, raw_val

    def extract_payloads(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract and parse all `[key:value, ...]` payload blocks in `text` using the
        quote-aware stateful parser.
        """
        payloads: List[Dict[str, Any]] = []
        for inner in self._iter_bracket_contents(text):
            inner_stripped = inner.strip()
            if not inner_stripped:
                continue
            kv_dict: Dict[str, Any] = {}
            for seg in self._split_top_level_comma(inner_stripped):
                parsed = self._parse_kv_item(seg)
                if parsed is not None:
                    k, v = parsed
                    kv_dict[k] = v
            if kv_dict:
                payloads.append(kv_dict)
        return payloads

    @staticmethod
    def format_payload(payload: Dict[str, Any]) -> str:
        """Serialize a payload dictionary back into `[k:v, ...]` with proper string quoting & escaping."""
        parts: List[str] = []
        for k, v in payload.items():
            if isinstance(v, str):
                escaped = v.replace("\\", "\\\\").replace('"', '\\"')
                parts.append(f'{k}:"{escaped}"')
            elif isinstance(v, bool):
                parts.append(f"{k}:{'true' if v else 'false'}")
            else:
                parts.append(f"{k}:{v}")
        return "[" + ", ".join(parts) + "]"

    def benchmark_compression(
        self,
        verbose_text: str,
        human_intent: str = "",
        on_oov: str = "nearest",
    ) -> Dict[str, Any]:
        """
        Multi-axis compression benchmark:
        1. Sacred (Verbose) -> Demotic Wire compression (`char_saving_percent` / `token_saving_percent`)
        2. End-to-End comparison against verbose Natural Language A2A JSON (`e2e_token_saving_percent`)
        3. Transparent OOV audit trail (`oov_substitutions` / `oov_repaired_count`)
        """
        compact_res = self.encode(verbose_text, on_oov=on_oov)
        compact_text = str(compact_res)
        oov_substitutions = list(compact_res.substitutions)

        # Measure Wire ID coverage outside quoted strings
        unquoted_compact = self._transform_outside_quotes(compact_text, lambda s: s)
        wire_syms = re.findall(r'§[A-Za-z0-9_]+', unquoted_compact)
        wire_compact_cnt = sum(
            1 for s in wire_syms
            if re.match(r'^§[A-Z][0-9]{2,4}$', s) and (s in self.compact_to_verbose or s in self.all_macros)
        )
        wire_coverage = round((wire_compact_cnt / len(wire_syms)) * 100.0, 2) if wire_syms else 100.0

        expanded_verbose = self.decode(compact_text, expand_macros=True)
        baseline_verbose = (
            expanded_verbose
            if re.search(r'§X\d{2,4}', compact_text)
            else self.decode(compact_text, expand_macros=False)
        )
        if len(verbose_text) > len(baseline_verbose):
            baseline_verbose = verbose_text

        orig_chars = len(baseline_verbose)
        comp_chars = len(compact_text)

        orig_bpe = count_bpe_tokens(baseline_verbose, "o200k_base")
        comp_bpe = count_bpe_tokens(compact_text, "o200k_base")
        orig_tokens = orig_bpe["tokens"]
        comp_tokens = comp_bpe["tokens"]

        char_saving = (1.0 - (comp_chars / orig_chars)) * 100.0 if orig_chars > 0 else 0.0
        token_saving = (1.0 - (comp_tokens / orig_tokens)) * 100.0 if orig_tokens > 0 else 0.0

        op_specs = []
        ja_specs = []
        for sym in re.findall(r'§[A-Za-z0-9_]+', expanded_verbose):
            if sym in self.definitions:
                d_en = self.definitions[sym].get("definition", "")
                d_ja = self.definitions[sym].get("japanese", "")
                if d_en:
                    op_specs.append(d_en)
                if d_ja:
                    ja_specs.append(d_ja)
        payloads = self.extract_payloads(verbose_text)
        eff_intent = human_intent.strip() if human_intent and human_intent.strip() else " / ".join(ja_specs)
        natural_a2a_envelope = {
            "protocol": "STANDARD_NATURAL_LANGUAGE_A2A_JSON",
            "rosetta_human_intent": eff_intent,
            "semantic_operation_specifications": op_specs,
            "structured_parameters": payloads,
        }
        natural_a2a_str = json.dumps(natural_a2a_envelope, ensure_ascii=False)
        e2e_natural_chars = len(natural_a2a_str)
        e2e_bpe = count_bpe_tokens(natural_a2a_str, "o200k_base")
        e2e_natural_tokens = max(orig_tokens, e2e_bpe["tokens"])
        e2e_token_saving = (
            (1.0 - (comp_tokens / e2e_natural_tokens)) * 100.0
            if e2e_natural_tokens > comp_tokens
            else token_saving
        )
        e2e_factor = round(e2e_natural_tokens / max(1, comp_tokens), 2)

        return {
            "verbose_len": orig_chars,
            "compact_len": comp_chars,
            "char_saving_percent": round(char_saving, 2),
            "verbose_est_tokens": orig_tokens,
            "compact_est_tokens": comp_tokens,
            "token_saving_percent": round(token_saving, 2),
            "e2e_natural_chars": e2e_natural_chars,
            "e2e_natural_est_tokens": e2e_natural_tokens,
            "e2e_token_saving_percent": round(e2e_token_saving, 2),
            "e2e_compression_factor": e2e_factor,
            "wire_id_coverage_percent": wire_coverage,
            "oov_repaired_count": len(oov_substitutions),
            "oov_substitutions": oov_substitutions,
            "substitutions": oov_substitutions,
            "tokenizer_encoding": comp_bpe["encoding"],
            "tokenizer_is_estimated": comp_bpe["is_estimated"],
            "payloads_preserved": payloads,
            "verbose_sample": baseline_verbose[:120],
            "compact_sample": compact_text[:120],
        }


if __name__ == "__main__":
    codec = ElegantCodec()
    test_str = '@CTX:FINANCIAL_TRADING :: §SYS_RESOURCE_ARBITER [target:"USD/JPY", limit:150.5, action:"HOLD", code:"007", note:"a, b", expr:"x]y", p:0.98] -[cost:0.02]-> §DATA_CAUSAL_TENSOR_MAP => §LOGIC_DEDUCTIVE_CONVERGENCE'
    compact = codec.encode(test_str)
    decoded = codec.decode(compact)
    bench = codec.benchmark_compression(test_str)

    print("=== Hybrid Payload Lossless Test (v5.4.2) ===")
    print("Original (Verbose):", test_str)
    print("Compact Wire ID:   ", compact)
    print("Decoded Back:      ", decoded)
    print("Extracted Payloads:", bench["payloads_preserved"])
    print(f"Compression stats:  {bench['char_saving_percent']}% char saved, {bench['token_saving_percent']}% token saved")

    assert test_str == decoded, "Lossless verification failed: decoded text does not match original!"
    print("✅ LOSSLESS ROUNDTRIP VERIFIED 100%!")
