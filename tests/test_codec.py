import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from codec import ElegantCodec, UnknownSymbolError, count_bpe_tokens


class TestElegantCodec(unittest.TestCase):
    def setUp(self):
        self.codec = ElegantCodec()

    def test_01_load_canonical_256_lexicon(self):
        """Canonical lexicon (256 primitives) loads accurately."""
        self.assertEqual(len(self.codec.definitions), 256)
        self.assertGreaterEqual(len(self.codec.verbose_to_compact), 256)
        self.assertEqual(len(self.codec.compact_to_verbose), 256)

    def test_02_missing_lexicon_path_raises_file_not_found(self):
        """Passing a non-existent lexicon path raises FileNotFoundError."""
        non_existent = REPO_ROOT / "lexicon" / "does_not_exist_12345.json"
        with self.assertRaises(FileNotFoundError):
            ElegantCodec(lexicon_path=non_existent)

    def test_03_env_var_missing_lexicon_raises_file_not_found(self):
        """Setting TOAI_LEXICON_PATH to a non-existent file raises FileNotFoundError."""
        old_val = os.environ.get("TOAI_LEXICON_PATH")
        try:
            os.environ["TOAI_LEXICON_PATH"] = "/tmp/non_existent_toai_lexicon_99999.json"
            with self.assertRaises(FileNotFoundError):
                ElegantCodec()
        finally:
            if old_val is None:
                os.environ.pop("TOAI_LEXICON_PATH", None)
            else:
                os.environ["TOAI_LEXICON_PATH"] = old_val

    def test_04_empty_lexicon_raises_runtime_error(self):
        """An empty lexicon JSON file is rejected with RuntimeError instead of failing silently."""
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as tmp:
            json.dump({"version": "5.4.2", "lexicon": {}}, tmp)
            tmp_path = Path(tmp.name)
        try:
            with self.assertRaises(RuntimeError):
                ElegantCodec(lexicon_path=tmp_path)
        finally:
            tmp_path.unlink(missing_ok=True)

    def test_05_readme_basic_example_roundtrip(self):
        """README canonical financial trading example round-trips 100% losslessly."""
        sacred_stmt = (
            '@CTX:FINANCIAL_TRADING :: '
            '§SYS_RESOURCE_ARBITER [target:"USD/JPY", limit:150.5, action:"HOLD", p:0.98] '
            '-[cost:0.02]-> §DATA_CAUSAL_TENSOR_MAP => §LOGIC_DEDUCTIVE_CONVERGENCE'
        )
        compact = self.codec.encode(sacred_stmt)
        self.assertIn("§S01", compact)
        self.assertIn("§D01", compact)
        self.assertIn("§L01", compact)
        decoded = self.codec.decode(compact)
        self.assertEqual(decoded, sacred_stmt)

    def test_06_quickstart_macro_statement_roundtrip(self):
        """Quickstart statement containing higher-order macro §X354 round-trips losslessly."""
        sacred_input = (
            '@CTX:DISTRIBUTED_RECOVERY :: '
            '§X354 [status:"degraded", threshold:0.85] '
            '-[p:0.99, c:0.01]-> §PROTO_GRACEFUL_DRAIN [action:"quiesce", timeout:15.0] '
            '!-> §PROTO_PARTIAL_COMMIT [partition:"edge-nodes"] '
            '? §SAFE_FALLBACK_HARMONY [mode:"safe"]'
        )
        wire = self.codec.encode(sacred_input)
        decoded = self.codec.decode(wire, expand_macros=False)
        self.assertEqual(decoded, sacred_input)

    def test_07_payload_leading_zero_string_preserved(self):
        """Quoted '007' stays string '007' while unquoted 007 / 42 become integers."""
        stmt = '@CTX:AUTH :: §SYS_RESOURCE_ARBITER [code:"007", raw_zero:007, count:42]'
        wire = self.codec.encode(stmt)
        decoded = self.codec.decode(wire)
        self.assertEqual(decoded, stmt)

        payloads = self.codec.extract_payloads(decoded)
        self.assertEqual(len(payloads), 1)
        self.assertEqual(payloads[0]["code"], "007")
        self.assertIsInstance(payloads[0]["code"], str)
        self.assertEqual(payloads[0]["raw_zero"], 7)
        self.assertIsInstance(payloads[0]["raw_zero"], int)
        self.assertEqual(payloads[0]["count"], 42)
        self.assertIsInstance(payloads[0]["count"], int)

    def test_08_payload_comma_inside_quotes_preserved(self):
        """Comma inside quoted value note:\"a, b\" is not split into multiple entries."""
        stmt = '@CTX:AUDIT :: §SYS_RESOURCE_ARBITER [note:"a, b", tag:"x, y, z", limit:150.5]'
        wire = self.codec.encode(stmt)
        decoded = self.codec.decode(wire)
        self.assertEqual(decoded, stmt)

        payloads = self.codec.extract_payloads(decoded)
        self.assertEqual(len(payloads), 1)
        self.assertEqual(payloads[0]["note"], "a, b")
        self.assertEqual(payloads[0]["tag"], "x, y, z")
        self.assertEqual(payloads[0]["limit"], 150.5)
        self.assertIsInstance(payloads[0]["limit"], float)

    def test_09_payload_closing_bracket_inside_quotes_preserved(self):
        """Closing bracket inside quoted value expr:\"x]y\" does not terminate the payload block."""
        stmt = '@CTX:PARSER :: §SYS_RESOURCE_ARBITER [expr:"x]y", arr:"a[0]b", step:1]'
        wire = self.codec.encode(stmt)
        decoded = self.codec.decode(wire)
        self.assertEqual(decoded, stmt)

        payloads = self.codec.extract_payloads(decoded)
        self.assertEqual(len(payloads), 1)
        self.assertEqual(payloads[0]["expr"], "x]y")
        self.assertEqual(payloads[0]["arr"], "a[0]b")
        self.assertEqual(payloads[0]["step"], 1)

    def test_10_payload_escaped_quotes_and_combined_special_cases(self):
        """Escaped quotes, commas, brackets, leading zeros, ints, and floats all work together."""
        stmt = (
            '@CTX:COMPLEX :: §SYS_RESOURCE_ARBITER '
            '[code:"007", note:"a, b", expr:"x]y", msg:"say \\"hello, [world]\\"", int_v:100, float_v:0.99]'
        )
        wire = self.codec.encode(stmt)
        decoded = self.codec.decode(wire)
        self.assertEqual(decoded, stmt)

        payloads = self.codec.extract_payloads(decoded)
        self.assertEqual(len(payloads), 1)
        p = payloads[0]
        self.assertEqual(p["code"], "007")
        self.assertEqual(p["note"], "a, b")
        self.assertEqual(p["expr"], "x]y")
        self.assertEqual(p["msg"], 'say "hello, [world]"')
        self.assertEqual(p["int_v"], 100)
        self.assertAlmostEqual(p["float_v"], 0.99)

    def test_11_on_oov_error_raises_unknown_symbol_error(self):
        """on_oov='error' (and default encode) raises UnknownSymbolError on unregistered symbol."""
        stmt = '@CTX:TEST :: §TOTALLY_NONEXISTENT_GIBBERISH_XYZ987 [k:1]'
        with self.assertRaises(UnknownSymbolError):
            self.codec.encode(stmt, on_oov="error")
        with self.assertRaises(UnknownSymbolError):
            self.codec.encode(stmt)

    def test_12_on_oov_keep_preserves_unknown_symbol(self):
        """on_oov='keep' keeps unknown symbols intact without collapsing them to §G01 or §OMEGA."""
        unknown_sym = "§CUSTOM_UNREGISTERED_SYMBOL_ZZZ"
        stmt = f'@CTX:TEST :: {unknown_sym} [code:"007"] => §LOGIC_DEDUCTIVE_CONVERGENCE'
        encoded = self.codec.encode(stmt, on_oov="keep")
        self.assertIn(unknown_sym, encoded)
        self.assertNotIn("§G01", encoded)
        self.assertNotIn("§OMEGA", encoded)
        self.assertIn("§L01", encoded)
        self.assertEqual(len(encoded.substitutions), 0)

    def test_13_on_oov_nearest_records_substitutions(self):
        """on_oov='nearest' resolves unknown symbols and records full history in substitutions."""
        unknown_sym = "§TOTALLY_ALIEN_SYMBOL_999"
        stmt = f'@CTX:TEST :: {unknown_sym} => §SYS_RESOURCE_ARBITER'
        encoded = self.codec.encode(stmt, on_oov="nearest")
        self.assertNotIn(unknown_sym, encoded)
        self.assertEqual(len(encoded.substitutions), 1)
        sub = encoded.substitutions[0]
        self.assertEqual(sub["original"], unknown_sym)
        self.assertTrue(sub["compact_id"].startswith("§"))
        self.assertTrue(sub["canonical"].startswith("§"))
        self.assertEqual(self.codec.last_substitutions, encoded.substitutions)

    def test_14_strict_risc_true_and_benchmark_oov_substitutions(self):
        """strict_risc=True triggers nearest OOV mode and benchmark_compression exposes oov_substitutions."""
        unknown_sym = "§LOGIC_CUSTOM_BAYESIAN_FOOBAR"
        stmt = f'@CTX:TEST :: {unknown_sym} [p:0.95] => §SYS_RESOURCE_ARBITER'
        encoded = self.codec.encode(stmt, strict_risc=True)
        self.assertEqual(len(encoded.oov_substitutions), 1)
        self.assertEqual(encoded.oov_substitutions[0]["original"], unknown_sym)

        bench = self.codec.benchmark_compression(stmt)
        self.assertIn("oov_substitutions", bench)
        self.assertEqual(len(bench["oov_substitutions"]), 1)
        self.assertEqual(bench["oov_substitutions"][0]["original"], unknown_sym)
        self.assertEqual(bench["oov_repaired_count"], 1)

    def test_15_symbols_inside_quoted_payload_are_not_mutated(self):
        """A §-prefixed string literal inside quotes is treated as payload data, not a wire symbol."""
        stmt = '@CTX:DOC :: §SYS_RESOURCE_ARBITER [example:"§UNKNOWN_IN_QUOTES", literal:"§S01"]'
        encoded = self.codec.encode(stmt, on_oov="error")
        self.assertIn('[example:"§UNKNOWN_IN_QUOTES", literal:"§S01"]', encoded)
        decoded = self.codec.decode(encoded)
        self.assertEqual(decoded, stmt)

    def test_16_count_bpe_tokens_helper(self):
        """count_bpe_tokens returns token count and estimation flag."""
        info = count_bpe_tokens("@CTX:FX :: §S01 [limit:150.5]", "o200k_base")
        self.assertIn("tokens", info)
        self.assertGreater(info["tokens"], 0)
        self.assertIn("is_estimated", info)
        self.assertIsInstance(info["is_estimated"], bool)


if __name__ == "__main__":
    unittest.main()
