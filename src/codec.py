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
        self.load_lexicon()

    def load_lexicon(self):
        if self.lexicon_path.exists():
            try:
                data = json.loads(self.lexicon_path.read_text(encoding="utf-8"))
                lex = data.get("lexicon", {})
                for sym, item in lex.items():
                    cid = item.get("compact_id")
                    if cid:
                        self.verbose_to_compact[sym] = cid
                        self.compact_to_verbose[cid] = sym
                    self.definitions[sym] = item
            except Exception as e:
                print(f"[ElegantCodec] Failed to load lexicon: {e}")

        if self.macro_path.exists():
            try:
                m_data = json.loads(self.macro_path.read_text(encoding="utf-8"))
                self.macros = m_data.get("macros", {})
            except Exception:
                pass

    def encode(self, text: str) -> str:
        """
        Verboseシンボル（§LOGIC_...）を最小BPEワイヤID（§L01等）に圧縮。
        ハイブリッド構文内の実務パラメータ [target:"USD/JPY", limit:150.5] は無傷で100%保持。
        """
        if not self.verbose_to_compact:
            self.load_lexicon()
        
        encoded = text
        # 長いシンボル名から順に置換
        sorted_symbols = sorted(self.verbose_to_compact.keys(), key=len, reverse=True)
        for sym in sorted_symbols:
            encoded = encoded.replace(sym, self.verbose_to_compact[sym])
        return encoded

    def decode(self, text: str) -> str:
        """
        CompactワイヤID（§L01等）を人間可読なVerboseシンボルへ復元。
        パラメータブラケット [...] 内のデータは1ビットの欠落もなく維持。
        """
        if not self.compact_to_verbose:
            self.load_lexicon()

        decoded = text
        # 正規表現で §[LSCDHGX][0-9]{2} を置換
        pattern = re.compile(r'§[A-Z][0-9]{2}')
        def replace_fn(match):
            cid = match.group(0)
            return self.compact_to_verbose.get(cid, cid)
        
        return pattern.sub(replace_fn, decoded)

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
        """文字数および概算トークン数の削減率を算出"""
        compact_text = self.encode(verbose_text)
        
        orig_chars = len(verbose_text)
        comp_chars = len(compact_text)
        
        char_saving = (1.0 - (comp_chars / orig_chars)) * 100.0 if orig_chars > 0 else 0.0
        
        return {
            "verbose_len": orig_chars,
            "compact_len": comp_chars,
            "char_saving_percent": round(char_saving, 2),
            "payloads_preserved": self.extract_payloads(verbose_text),
            "verbose_sample": verbose_text[:120],
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
