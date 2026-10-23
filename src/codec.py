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

    def encode(self, text: str) -> str:
        """
        Verboseシンボル（§LOGIC_...）を最小BPEワイヤID（§L01等）に圧縮。
        ハイブリッド構文内の実務パラメータ [target:"USD/JPY", limit:150.5] は無傷で100%保持。
        """
        if not self.verbose_to_compact:
            self.load_lexicon()

        # 単語境界を厳守した1パス正規表現置換（§RESO が §RESONANCE_NEXUS の先頭を破壊する部分一致バグを完全防止）
        token_pattern = re.compile(r'§[A-Za-z0-9_]+')
        def encode_token(match):
            sym = match.group(0)
            # 既に Compact Wire ID (§L01, §X64 等) の場合はそのまま維持
            if re.match(r'^§[A-Z][0-9]{2,4}$', sym):
                return sym
            if sym in self.verbose_to_compact:
                return self.verbose_to_compact[sym]
            if sym in self.macro_name_to_id:
                return self.macro_name_to_id[sym]
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

    def benchmark_compression(self, verbose_text: str) -> dict:
        """文字数および推定BPEトークン数の削減率を算出（高次マクロ §X.. 使用時は展開後ベースラインと比較）"""
        compact_text = self.encode(verbose_text)
        # マクロ(§X..)が含まれる場合は展開後Verbose表現をベースラインとして真の圧縮率を評価
        baseline_verbose = self.decode(compact_text, expand_macros=True) if re.search(r'§X\d{2,4}', compact_text) else self.decode(compact_text, expand_macros=False)
        if len(verbose_text) > len(baseline_verbose):
            baseline_verbose = verbose_text

        orig_chars = len(baseline_verbose)
        comp_chars = len(compact_text)
        orig_tokens = self.estimate_bpe_tokens(baseline_verbose)
        comp_tokens = self.estimate_bpe_tokens(compact_text)

        char_saving = (1.0 - (comp_chars / orig_chars)) * 100.0 if orig_chars > 0 else 0.0
        token_saving = (1.0 - (comp_tokens / orig_tokens)) * 100.0 if orig_tokens > 0 else 0.0

        return {
            "verbose_len": orig_chars,
            "compact_len": comp_chars,
            "char_saving_percent": round(char_saving, 2),
            "verbose_est_tokens": orig_tokens,
            "compact_est_tokens": comp_tokens,
            "token_saving_percent": round(token_saving, 2),
            "payloads_preserved": self.extract_payloads(verbose_text),
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
