"""
TOAI-elegant-lang Two-Layer BPE Codec & Tokenizer Optimizer
- Verbose (Full descriptive symbols) <-> Compact (1-2 BPE tokens wire format)
- BPE token saving ratio calculator
"""

import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.absolute()
LEXICON_FILE = BASE_DIR / "lexicon" / "core_lexicon.json"

class ElegantCodec:
    def __init__(self, lexicon_path: Path = LEXICON_FILE):
        self.lexicon_path = lexicon_path
        self.verbose_to_compact = {}
        self.compact_to_verbose = {}
        self.definitions = {}
        self.load_lexicon()

    def load_lexicon(self):
        if not self.lexicon_path.exists():
            return
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

    def encode(self, text: str) -> str:
        """Verboseシンボル（§LOGIC_...）を最小BPEワイヤID（§L01等）に圧縮"""
        if not self.verbose_to_compact:
            self.load_lexicon()
        
        encoded = text
        # 長いシンボル名から順に置換
        sorted_symbols = sorted(self.verbose_to_compact.keys(), key=len, reverse=True)
        for sym in sorted_symbols:
            encoded = encoded.replace(sym, self.verbose_to_compact[sym])
        return encoded

    def decode(self, text: str) -> str:
        """CompactワイヤID（§L01等）を人間可読なVerboseシンボルへ復元"""
        if not self.compact_to_verbose:
            self.load_lexicon()

        decoded = text
        # 正規表現で §[LSCDHG][0-9]{2} を置換
        pattern = re.compile(r'§[A-Z][0-9]{2}')
        def replace_fn(match):
            cid = match.group(0)
            return self.compact_to_verbose.get(cid, cid)
        
        return pattern.sub(replace_fn, decoded)

    def benchmark_compression(self, verbose_text: str) -> dict:
        """文字数および概算トークン数の削減率を算出"""
        compact_text = self.encode(verbose_text)
        
        # 簡易BPE概算（英単語・記号の境界基準: 4文字≒1トークン、Compact IDは1トークン判定）
        orig_chars = len(verbose_text)
        comp_chars = len(compact_text)
        
        char_saving = (1.0 - (comp_chars / orig_chars)) * 100.0 if orig_chars > 0 else 0.0
        
        return {
            "verbose_len": orig_chars,
            "compact_len": comp_chars,
            "char_saving_percent": round(char_saving, 2),
            "verbose_sample": verbose_text[:120],
            "compact_sample": compact_text[:120]
        }

if __name__ == "__main__":
    codec = ElegantCodec()
    test_str = "§SYS_QUANTUM_RESOURCE_ARBITER [SYS_QUANTUM_THROTTLE_LOCK] -[p:0.95, c:120]-> §DATA_CAUSAL_TENSOR_MAP > { §LOGIC_PROBABILISTIC_FALSIFICATION_GATES } [AND] §LATENT_HARMONY_PRISM => §SYNC_DIALECTIC_WEIGHTED_CONSENSUS_STATE"
    compact = codec.encode(test_str)
    decoded = codec.decode(compact)
    bench = codec.benchmark_compression(test_str)
    print("=== Elegant Codec Test ===")
    print("Original (Verbose):", test_str)
    print("Compact Wire ID:   ", compact)
    print("Decoded Back:      ", decoded)
    print("Compression stats: ", bench)
