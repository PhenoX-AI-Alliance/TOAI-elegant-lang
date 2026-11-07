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

    def test_17_all_lexicons_and_corpus_symbols_strict_uppercase_and_defined(self):
        """
        v5.4.3 Step 1: Verify that all 3 dictionaries (core_lexicon.json, macro_lexicon.json,
        rosetta_layer.json in both lexicon/ and src/lexicon/) and corpus/dialogues.jsonl
        contain zero lowercase characters (e.g. GAiar, _v2), zero CJK corruption, and zero
        undefined §-symbols.
        """
        import re

        strict_sym_re = re.compile(r"^§[A-Z][A-Z0-9_]*$")
        any_sym_re = re.compile(r"§[A-Za-z0-9_\u4e00-\u9fff]+")

        def is_registered(sym: str) -> bool:
            return (
                sym in self.codec.compact_to_verbose
                or sym in self.codec.verbose_to_compact
                or sym in self.codec.definitions
                or sym in self.codec.all_macros
                or sym in self.codec.macro_name_to_id
            )

        dict_paths = [
            REPO_ROOT / "lexicon" / "core_lexicon.json",
            REPO_ROOT / "lexicon" / "macro_lexicon.json",
            REPO_ROOT / "lexicon" / "rosetta_layer.json",
            REPO_ROOT / "src" / "lexicon" / "core_lexicon.json",
            REPO_ROOT / "src" / "lexicon" / "macro_lexicon.json",
            REPO_ROOT / "src" / "lexicon" / "rosetta_layer.json",
        ]
        for dp in dict_paths:
            self.assertTrue(dp.is_file(), f"Missing dictionary file: {dp}")
            raw = dp.read_text(encoding="utf-8")
            self.assertNotIn("GAiar", raw, f"Typo GAiar found in {dp}")
            self.assertNotIn("ERECVERY", raw, f"Typo ERECVERY found in {dp}")
            data = json.loads(raw)
            serialized = json.dumps(data, ensure_ascii=False)
            for sym in set(any_sym_re.findall(serialized)):
                self.assertRegex(sym, strict_sym_re, f"Invalid symbol '{sym}' in {dp}")
                self.assertTrue(is_registered(sym), f"Unregistered symbol '{sym}' in {dp}")

        # Verify all macro expansions decode cleanly into strict uppercase symbols
        for mid in self.codec.all_macros:
            expanded = self.codec.resolve_macro(mid)
            for sym in any_sym_re.findall(expanded):
                self.assertRegex(sym, strict_sym_re, f"Invalid symbol '{sym}' in macro {mid}")
                self.assertTrue(is_registered(sym), f"Unregistered symbol '{sym}' in macro {mid}")

        # Verify corpus/dialogues.jsonl
        corpus_path = REPO_ROOT / "corpus" / "dialogues.jsonl"
        self.assertTrue(corpus_path.is_file())
        raw_corpus = corpus_path.read_text(encoding="utf-8")
        self.assertNotIn("GAiar", raw_corpus, "Typo GAiar found in corpus/dialogues.jsonl")
        for line_no, line in enumerate(raw_corpus.splitlines(), 1):
            if not line.strip():
                continue
            row = json.loads(line)
            for field_name in ("compact_wire", "raw"):
                val = row.get(field_name, "")
                if not isinstance(val, str):
                    continue
                for sym in re.findall(r"§[A-Za-z0-9_]+", val):
                    self.assertRegex(
                        sym,
                        strict_sym_re,
                        f"Line {line_no} field '{field_name}' has non-uppercase symbol '{sym}'",
                    )
                    self.assertTrue(
                        is_registered(sym),
                        f"Line {line_no} field '{field_name}' has undefined symbol '{sym}'",
                    )

    def test_18_independent_corpus_audit_and_comprehension_harness(self):
        """
        v5.4.3 Step 2 & Step 3: Verify independent corpus alignment auditor, Cohen's kappa,
        and eval_comprehension Conditions A-E, Wilson CI, and McNemar test.
        """
        if str(REPO_ROOT) not in sys.path:
            sys.path.insert(0, str(REPO_ROOT))
        from src.audit_corpus_alignment import audit_record, get_tag_to_domain, score_human_audit_sample
        from benchmarks.eval_comprehension import (
            build_for_condition,
            load_items,
            mcnemar_test,
            select_stratified_items,
            wilson,
        )

        tag_to_dom = get_tag_to_domain()
        # Q3-like mismatch: FX scenario with only recovery primitives must be flagged MISMATCH
        bad_fx = {
            "scenario": "【実務・FX自動売買】為替レート急変時に、リスクパラメータを相手ノードへ渡し、緊急ヘッジ取引の合意を形成する",
            "compact_wire": ":: §G50 => §G48 => §G51",
        }
        res_fx = audit_record(self.codec, bad_fx, tag_to_dom)
        self.assertIsNotNone(res_fx)
        self.assertEqual(res_fx["machine_verdict"], "MISMATCH")
        self.assertIn("Recovery Pattern Leak", res_fx["mismatch_reason"])

        # Q18-like mismatch: Parser scenario with ARBITRAGE (§S02) must be flagged MISMATCH (Domain Bleed)
        bad_parser = {
            "scenario": "【実務・コード生成委譲】構文パーサーのバグ修正タスクを委譲し、型整合性のテスト完了を要求する",
            "compact_wire": ":: §S02 --> §G09 => §G15",
        }
        res_parser = audit_record(self.codec, bad_parser, tag_to_dom)
        self.assertIsNotNone(res_parser)
        self.assertEqual(res_parser["machine_verdict"], "MISMATCH")
        self.assertIn("Domain Bleed", res_parser["mismatch_reason"])

        # Human audit sample CSV kappa scoring
        sample_csv = REPO_ROOT / "corpus" / "human_audit_sample.csv"
        if sample_csv.is_file():
            kappa_res = score_human_audit_sample(sample_csv)
            self.assertEqual(kappa_res["n"], 60)
            self.assertGreater(kappa_res["cohens_kappa"], 0.7)

        # Wilson CI & McNemar test
        lo, hi = wilson(16, 23)
        self.assertAlmostEqual(lo, 0.49, delta=0.02)
        self.assertAlmostEqual(hi, 0.84, delta=0.02)

        mcn = mcnemar_test([False] * 10 + [True] * 10, [True] * 20)
        self.assertEqual(mcn["b_only_first_correct"], 0)
        self.assertEqual(mcn["c_only_second_correct"], 10)
        self.assertTrue(mcn["significant_p05"])

        # Build Conditions A-E in temporary directory
        items = load_items(self.codec)
        chosen = select_stratified_items(items, 8, seed=7)
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_out = Path(tmpdir)
            for c in ("A", "B", "C", "D", "E"):
                meta = build_for_condition(self.codec, items, chosen, c, 7, tmp_out)
                self.assertEqual(meta["n_total_prompts"], 8)
                self.assertTrue((tmp_out / f"questions_{c}.md").is_file())
            meta_rot = build_for_condition(
                self.codec, items, chosen, "B", 7, tmp_out, keep_ctx=True, rotate_options=True
            )
            self.assertEqual(meta_rot["n_total_prompts"], 32)
            self.assertEqual(meta_rot["protocol_mode"], "protocol_header_keep_ctx")

        # v5.4.4: Verify N=112 disjoint holdout corpus independence & compression-accuracy tradeoff
        from src.audit_corpus_alignment import verify_holdout_independence
        from benchmarks.fair_bench import evaluate_compression_task_tradeoff

        holdout_path = REPO_ROOT / "corpus" / "holdout_comprehension.jsonl"
        self.assertTrue(holdout_path.is_file(), "holdout_comprehension.jsonl must exist")
        ind_res = verify_holdout_independence(
            self.codec, REPO_ROOT / "corpus" / "dialogues.jsonl", holdout_path
        )
        self.assertEqual(ind_res["holdout_rows"], 112)
        self.assertEqual(ind_res["exact_wire_overlap_count"], 0)
        self.assertEqual(ind_res["skeletal_wire_overlap_count"], 0)
        self.assertEqual(ind_res["repair_scenario_overlap_count"], 0)
        self.assertEqual(ind_res["holdout_ontology_alignment_pct"], 100.0)
        self.assertTrue(ind_res["strictly_independent"])

        tradeoff = evaluate_compression_task_tradeoff(self.codec)
        self.assertEqual(len(tradeoff), 7)
        toai_row = [r for r in tradeoff if "TOAI Demotic Wire" in r["method"]][0]
        self.assertEqual(toai_row["syntax_parse_rate_pct"], 100.0)
        self.assertEqual(toai_row["numeric_param_fidelity_pct"], 100.0)
        self.assertEqual(toai_row["task_ast_execution_acc_pct"], 100.0)


if __name__ == "__main__":
    unittest.main()
