"""
TOAI-elegant-lang Two-Layer BPE Codec & Tokenizer Optimizer
- Verbose (Full descriptive symbols) <-> Compact (1-2 BPE tokens wire format)
- Hybrid Payload Syntax: e.g. [target:"USD/JPY", limit:150.5, action:"HOLD"] lossless parameters
- BPE token saving ratio calculator
"""

import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.absolute()
LEXICON_FILE = BASE_DIR / "lexicon" / "core_lexicon.json"
MACRO_FILE = BASE_DIR / "lexicon" / "macro_lexicon.json"

class ElegantCodec:
    def __init__(self, lexicon_path: Path = LEXICON_FILE, macro_path: Path = MACRO_FILE):
        self.lexicon_path = lexicon_path
        self.macro_path = macro_path
        self.verbose_to_compact = {}
        self.compact_to_verbose = {}
        self.definitions = {}
        self.macros = {}
        self.archived_macros = {}
        self.all_macros = {}
        self.macro_name_to_id = {}
        self.load_lexicon()

    def load_lexicon(self):
        self.verbose_to_compact = {}
        self.compact_to_verbose = {}
        self.definitions = {}
        self.macros = {}
        self.archived_macros = {}
        self.all_macros = {}
        self.macro_name_to_id = {}
        if self.lexicon_path.exists():
            try:
                data = json.loads(self.lexicon_path.read_text(encoding="utf-8"))
                lex = data.get("lexicon", {})
                for sym, item in lex.items():
                    cid = item.get("compact_id")
                    if cid:
                        self.verbose_to_compact[sym] = cid
                        self.compact_to_verbose[cid] = sym
                        # Phase 1.5 / 1.6 リファクタリング済み旧シンボルの後方互換エイリアスも登録
                        for alias in item.get("aliases", []):
                            if alias not in self.verbose_to_compact:
                                self.verbose_to_compact[alias] = cid
                    self.definitions[sym] = item
            except Exception as e:
                print(f"[ElegantCodec] Failed to load lexicon: {e}")

        if self.macro_path.exists():
            try:
                m_data = json.loads(self.macro_path.read_text(encoding="utf-8"))
                self.macros = m_data.get("macros", {})
                self.archived_macros = m_data.get("archived_macros", {})
                # アクティブ枠(上位256)とアーカイブ退避枠の両方を統合してデコード互換性を永久保証
                self.all_macros = {**self.archived_macros, **self.macros}
                for mid, m_item in self.all_macros.items():
                    m_name = str(m_item.get("name", "")).strip()
                    if m_name and re.match(r'^§?[A-Z0-9_]+$', m_name):
                        norm_name = m_name if m_name.startswith("§") else f"§{m_name}"
                        if norm_name not in self.verbose_to_compact:
                            self.macro_name_to_id[norm_name] = mid
            except Exception:
                pass

    def resolve_nearest_primitive(self, oov_symbol: str) -> tuple:
        """
        Strict RISC OOV リゾルバ:
        未登録の §... 造語（OOV）が出力された場合、形態素・語幹(4文字)・カテゴリ・英語定義照合により
        256基本プリミティブ（またはアクティブマクロ）の中から最も意味的に近い正規シンボルと Compact Wire ID を決定論的に返す。
        これにより Demotic Wire 上での未変換フルスペル語（OOV率）を 0.0%（100% ワイヤID化）に保証する。
        """
        if not self.verbose_to_compact:
            self.load_lexicon()

        sym = oov_symbol.strip()
        if not sym.startswith("§"):
            sym = "§" + sym

        # 1. 既知の Compact ID の場合
        if re.match(r'^§[A-Z][0-9]{2,4}$', sym):
            if sym in self.compact_to_verbose:
                return self.compact_to_verbose[sym], sym
            if sym in self.all_macros:
                return sym, sym

        # 2. 既知の正規シンボルまたはエイリアス・マクロ名の場合
        if sym in self.verbose_to_compact:
            cid = self.verbose_to_compact[sym]
            canon = self.compact_to_verbose.get(cid, sym)
            return canon, cid
        if sym in self.macro_name_to_id:
            mid = self.macro_name_to_id[sym]
            return mid, mid

        # 3. 形態素・語幹・意味定義マッチングによる最近傍256プリミティブ探索
        raw_tokens = [t.upper() for t in re.split(r'_+', sym[1:]) if t]
        token_set = set(raw_tokens)
        stem_set = {t[:4] for t in raw_tokens if len(t) >= 4}

        # 先頭ドメインヒント推定
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
        best_score = -1.0

        for cand_sym, item in self.definitions.items():
            cid = item.get("compact_id")
            if not cid:
                continue
            cand_tokens = [t.upper() for t in re.split(r'_+', cand_sym[1:]) if t]
            cand_set = set(cand_tokens)
            cand_stems = {t[:4] for t in cand_tokens if len(t) >= 4}

            # エイリアス内のトークンも加味
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

    def normalize_to_strict_risc(self, text: str) -> tuple:
        """
        Strict RISC ポストプロセッサ:
        文中の未登録造語（OOV）や旧エイリアス名を256正規プリミティブ（またはアクティブマクロ）へ正規化し、
        (正規化後テキスト, [(旧トークン, 正規化後トークン), ...]) を返す。
        """
        if not self.verbose_to_compact:
            self.load_lexicon()

        replacements = []
        token_pattern = re.compile(r'§[A-Za-z0-9_]+')

        def replace_oov(match):
            sym = match.group(0)
            if re.match(r'^§[A-Z][0-9]{2,4}$', sym):
                if sym in self.compact_to_verbose or sym in self.all_macros:
                    return sym
            if sym in self.definitions:
                return sym
            if sym in self.macro_name_to_id:
                mid = self.macro_name_to_id[sym]
                replacements.append((sym, mid))
                return mid
            canon_sym, _ = self.resolve_nearest_primitive(sym)
            if canon_sym != sym:
                replacements.append((sym, canon_sym))
            return canon_sym

        normalized = token_pattern.sub(replace_oov, text)
        return normalized, replacements

    def encode(self, text: str, strict_risc: bool = True) -> str:
        """
        Verboseシンボル（§LOGIC_...）を最小BPEワイヤID（§L01等）に圧縮。
        strict_risc=True（デフォルト）により、万が一未登録の §... 造語（OOV）が含まれていても
        最近傍の正規プリミティブの Compact Wire ID へ100%変換し、Wire上のOOV率 0% を保証する。
        ハイブリッド構文内の実務パラメータ [target:"USD/JPY", limit:150.5] は無傷で100%保持。
        """
        if not self.verbose_to_compact:
            self.load_lexicon()

        # 単語境界を厳守した1パス正規表現置換
        token_pattern = re.compile(r'§[A-Za-z0-9_]+')
        def encode_token(match):
            sym = match.group(0)
            # 既に有効な Compact Wire ID (§L01, §X64 等) の場合はそのまま維持
            if re.match(r'^§[A-Z][0-9]{2,4}$', sym):
                if sym in self.compact_to_verbose or sym in self.all_macros or not strict_risc:
                    return sym
            if sym in self.verbose_to_compact:
                return self.verbose_to_compact[sym]
            if sym in self.macro_name_to_id:
                return self.macro_name_to_id[sym]
            if strict_risc:
                _, nearest_cid = self.resolve_nearest_primitive(sym)
                return nearest_cid
            return sym

        return token_pattern.sub(encode_token, text)

    def resolve_macro(self, macro_id: str) -> str:
        """アクティブおよびアーカイブ済みマクロIDを展開式（Verboseシンボル）へ完全復元"""
        m_item = self.all_macros.get(macro_id)
        if not m_item:
            return macro_id
        exp = m_item.get("expansion", "")
        if not exp:
            return macro_id
        # 展開式内の基本ワイヤIDもVerboseへ復元
        prim_pattern = re.compile(r'§[LSCDHG][0-9]{2,4}')
        return prim_pattern.sub(lambda m: self.compact_to_verbose.get(m.group(0), m.group(0)), exp)

    def decode(self, text: str, expand_macros: bool = False) -> str:
        """
        CompactワイヤID（§L01等）を人間可読なVerboseシンボルへ復元。
        expand_macros=True の場合、アクティブ・アーカイブ退避済みの §X.. マクロも展開式へ完全復元。
        パラメータブラケット [...] 内のデータは1ビットの欠落もなく維持。
        """
        if not self.compact_to_verbose:
            self.load_lexicon()

        decoded = text
        # 正規表現で単語境界付きの §[A-Z][0-9]{2,4} を一括置換（3桁ID §X100 等での部分一致バグを防止）
        pattern = re.compile(r'§[A-Z][0-9]{2,4}(?![A-Za-z0-9_])')
        def replace_fn(match):
            cid = match.group(0)
            if cid.startswith("§X") and expand_macros and cid in self.all_macros:
                return f"({self.resolve_macro(cid)})"
            return self.compact_to_verbose.get(cid, cid)
        
        return pattern.sub(replace_fn, decoded)

    @staticmethod
    def estimate_bpe_tokens(text: str) -> int:
        """
        標準BPEトークナイザー（cl100k / SentencePiece相当）のサブワード分割特性に基づくトークン数推定:
        - '§' 記号: 1 token
        - 英字サブワード（約4文字単位 / アンダースコア区切り）: 1 token each
        - 数値チャンク（1〜3桁）: 1 token
        - 句読点・演算子・非空白記号: 1 token
        - CJK文字: 約1.2 token
        """
        if not text:
            return 0
        # 全大文字定数(UPPER_SNAKE)はBPE上で2〜3文字単位に細分化される特性を反映
        chunks = re.findall(r'§|_[A-Z]{1,2}|[A-Z]{1,3}|[a-z]{1,4}|[0-9]{1,3}|[\u3000-\u9fff]|[^\sA-Za-z0-9§\u3000-\u9fff]', text)
        return max(1, len(chunks))

    def extract_payloads(self, text: str) -> list:
        """メッセージ内の実務パラメータ [key:value, ...] を抽出・パース"""
        payloads = []
        # ブラケット内の key:value を抽出
        for m in re.finditer(r'\[(.*?)\]', text):
            inner = m.group(1).strip()
            # 確率パラメータ (p:0.95, c:12) や実務パラメータ (target:"USD/JPY") を解析
            kv_dict = {}
            for item in re.split(r',\s*', inner):
                if ':' in item:
                    k, v = item.split(':', 1)
                    k = k.strip()
                    v = v.strip().strip('"\'')
                    # 数値変換試行
                    try:
                        if '.' in v:
                            v = float(v)
                        else:
                            v = int(v)
                    except ValueError:
                        pass
                    kv_dict[k] = v
            if kv_dict:
                payloads.append(kv_dict)
        return payloads

    def benchmark_compression(self, verbose_text: str, human_intent: str = "") -> dict:
        """
        二軸圧縮ベンチマーク計測:
        1. Sacred (Verbose) -> Demotic Wire 単体圧縮率 (char_saving_percent / token_saving_percent)
        2. 通常の自然言語A2A通信（Rosetta Intent自然文＋意味仕様定義＋構造化JSONペイロード）と比較した
           対自然言語 End-to-End トークン削減率 (e2e_token_saving_percent) およびコンテキスト圧縮倍率 (e2e_compression_factor)
        """
        _, oov_repairs = self.normalize_to_strict_risc(verbose_text)
        compact_text = self.encode(verbose_text, strict_risc=True)

        # Wire上の全 § トークンが Compact ID 化されている割合を算出
        wire_syms = re.findall(r'§[A-Za-z0-9_]+', compact_text)
        wire_compact_cnt = sum(1 for s in wire_syms if re.match(r'^§[A-Z][0-9]{2,4}$', s))
        wire_coverage = round((wire_compact_cnt / len(wire_syms)) * 100.0, 2) if wire_syms else 100.0

        # マクロ(§X..)が含まれる場合は展開後Verbose表現をベースラインとして真の圧縮率を評価
        expanded_verbose = self.decode(compact_text, expand_macros=True)
        baseline_verbose = expanded_verbose if re.search(r'§X\d{2,4}', compact_text) else self.decode(compact_text, expand_macros=False)
        if len(verbose_text) > len(baseline_verbose):
            baseline_verbose = verbose_text

        orig_chars = len(baseline_verbose)
        comp_chars = len(compact_text)
        orig_tokens = self.estimate_bpe_tokens(baseline_verbose)
        comp_tokens = self.estimate_bpe_tokens(compact_text)

        char_saving = (1.0 - (comp_chars / orig_chars)) * 100.0 if orig_chars > 0 else 0.0
        token_saving = (1.0 - (comp_tokens / orig_tokens)) * 100.0 if orig_tokens > 0 else 0.0

        # 対自然言語 End-to-End (E2E) ベースライン算出:
        # 同じ業務意図・プリミティブ仕様定義・構造化JSONパラメータを通常の自然言語A2A JSONで送った場合のトークン数
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
            "structured_parameters": payloads
        }
        natural_a2a_str = json.dumps(natural_a2a_envelope, ensure_ascii=False)
        e2e_natural_chars = len(natural_a2a_str)
        e2e_natural_tokens = max(orig_tokens, self.estimate_bpe_tokens(natural_a2a_str))
        e2e_token_saving = (1.0 - (comp_tokens / e2e_natural_tokens)) * 100.0 if e2e_natural_tokens > comp_tokens else token_saving
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
            "oov_repaired_count": len(oov_repairs),
            "payloads_preserved": payloads,
            "verbose_sample": baseline_verbose[:120],
            "compact_sample": compact_text[:120]
        }

if __name__ == "__main__":
    codec = ElegantCodec()
    test_str = '@CTX:FINANCIAL_TRADING :: §SYS_RESOURCE_ARBITER [target:"USD/JPY", limit:150.5, action:"HOLD", p:0.98] -[cost:0.02]-> §DATA_CAUSAL_TENSOR_MAP => §LOGIC_DEDUCTIVE_CONVERGENCE'
    compact = codec.encode(test_str)
    decoded = codec.decode(compact)
    bench = codec.benchmark_compression(test_str)
    
    print("=== Hybrid Payload Lossless Test ===")
    print("Original (Verbose):", test_str)
    print("Compact Wire ID:   ", compact)
    print("Decoded Back:      ", decoded)
    print("Extracted Payloads:", bench["payloads_preserved"])
    print(f"Compression stats:  {bench['char_saving_percent']}% saved")
    
    # ロスレス検証アサート
    assert test_str == decoded, "Lossless verification failed: decoded text does not match original!"
    print("✅ LOSSLESS ROUNDTRIP VERIFIED 100%!")
