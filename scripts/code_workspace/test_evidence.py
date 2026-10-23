"""Negative acceptance receipts: stale/missing/failing evidence must fail closed."""

import copy
import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

try:
    from . import evidence
except ImportError:
    import evidence


class GeneratorEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.parts = {"isolated": {"schemaVersion": 1, "entries": [{"code": "é"}]}}
        sha = evidence.digest_text(
            json.dumps(
                self.parts["isolated"]["entries"], sort_keys=True, ensure_ascii=False
            )
        )
        self.generators = {
            "isolated": {
                "success": True,
                "pairs": 1,
                "savedSha256": sha,
                "generatedSha256": sha,
            }
        }

    def test_generator_hashes_bind_entry_list_not_enclosing_part(self):
        evidence.generator_evidence(self.parts, self.generators)

    def test_changed_entry_is_rejected(self):
        self.parts["isolated"]["entries"][0]["code"] = "changed"
        with self.assertRaisesRegex(evidence.EvidenceError, "stale/failing"):
            evidence.generator_evidence(self.parts, self.generators)

    def test_missing_failed_or_wrong_count_regeneration_is_rejected(self):
        for update in ({"success": False}, {"pairs": 2}, {"generatedSha256": "0" * 64}):
            with self.subTest(update=update):
                rows = copy.deepcopy(self.generators)
                rows["isolated"].update(update)
                with self.assertRaisesRegex(evidence.EvidenceError, "stale/failing"):
                    evidence.generator_evidence(self.parts, rows)
        with self.assertRaisesRegex(evidence.EvidenceError, "omitted"):
            evidence.generator_evidence(self.parts, {})


class EvidenceSelectionTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix="callable-evidence-test-")
        self.root = Path(self.directory.name)
        self.key = ("problem", "java", "solution")

    def tearDown(self):
        self.directory.cleanup()

    def report(self, name, rows, stamp, fingerprint="current"):
        path = self.root / name
        path.write_text(
            json.dumps({"fingerprint": fingerprint, "executions": rows}),
            encoding="utf-8",
        )
        os.utime(path, ns=(stamp, stamp))
        return path

    def row(self, accepted=True, key=None):
        pid, language, role = key or self.key
        return {
            "problemId": pid,
            "language": language,
            "role": role,
            "accepted": accepted,
        }

    def collect(self, paths, expected=None):
        return evidence.collect_current_rows(
            paths,
            expected or {self.key},
            lambda report: report["fingerprint"] == "current",
            lambda row: (row["problemId"], row["language"], row["role"]),
            lambda row, _: (
                [] if row["accepted"] else ["a real current execution failed"]
            ),
            "executions",
            "Test receipt matrix",
            self.root,
        )

    def test_later_failure_invalidates_older_current_pass(self):
        passed = self.report("older-pass.json", [self.row()], 100)
        failed = self.report("later-failure.json", [self.row(False)], 200)
        with self.assertRaisesRegex(evidence.EvidenceError, "later-failure.json"):
            self.collect([passed, failed])

    def test_stale_later_pass_cannot_hide_current_failure(self):
        passed = self.report("older-pass.json", [self.row()], 100)
        failed = self.report("current-failure.json", [self.row(False)], 200)
        stale = self.report(
            "stale-pass.json", [self.row()], 300, fingerprint="old source"
        )
        with self.assertRaisesRegex(evidence.EvidenceError, "current-failure.json"):
            self.collect([passed, stale, failed])

    def test_new_current_rerun_can_repair_a_failure(self):
        failed = self.report("failed.json", [self.row(False)], 100)
        passed = self.report("rerun.json", [self.row()], 200)
        accepted, stale = self.collect([passed, failed])
        self.assertEqual(stale, 0)
        self.assertEqual(accepted[self.key]["evidence"]["path"], "rerun.json")

    def test_equal_timestamp_failure_wins(self):
        failed = self.report("a-failed.json", [self.row(False)], 100)
        passed = self.report("z-passed.json", [self.row()], 100)
        with self.assertRaisesRegex(evidence.EvidenceError, "a-failed.json"):
            self.collect([failed, passed])

    def test_missing_language_or_role_is_not_optional(self):
        passed = self.report("one-role.json", [self.row()], 100)
        expected = {
            self.key,
            ("problem", "java", "starter"),
            ("problem", "cpp", "solution"),
        }
        with self.assertRaisesRegex(
            evidence.EvidenceError, "2 missing/current failing scopes"
        ):
            self.collect([passed], expected)

    def test_duplicate_execution_cannot_fill_missing_coverage(self):
        path = self.report("duplicate.json", [self.row(), self.row()], 100)
        with self.assertRaisesRegex(evidence.EvidenceError, "duplicate scope"):
            self.collect([path])

    def test_only_stale_pass_is_not_acceptance(self):
        path = self.report("stale.json", [self.row()], 100, fingerprint="old source")
        with self.assertRaisesRegex(evidence.EvidenceError, "missing current evidence"):
            self.collect([path])


class JudgeContractTests(unittest.TestCase):
    @staticmethod
    def receipt(status="Accepted", passed=3, cases=None):
        return {
            "success": True,
            "failure": None,
            "result": {
                "Status": status,
                "Passed": passed,
                "Total": 3,
                "Cases": cases or [],
            },
        }

    def test_starter_must_reach_judge_instead_of_compile_or_timeout(self):
        for status in (
            "Compilation error",
            "Time limit exceeded",
            "Toolchain unavailable",
            "Runtime error",
        ):
            with self.subTest(status=status):
                self.assertTrue(
                    evidence.result_errors(self.receipt(status, 0), 3, "starter")
                )
        self.assertEqual(
            evidence.result_errors(
                self.receipt("Runtime error", 0, [{"Number": 1}]), 3, "starter"
            ),
            [],
        )

    def test_accepted_starter_requires_full_corpus(self):
        self.assertTrue(evidence.result_errors(self.receipt(passed=2), 3, "starter"))
        self.assertEqual(evidence.result_errors(self.receipt(), 3, "starter"), [])

    def test_incorrect_algorithm_must_fail_a_real_case(self):
        for row in (
            self.receipt(),
            self.receipt("Compilation error", 0),
            self.receipt("Wrong answer", 0),
        ):
            self.assertTrue(evidence.result_errors(row, 3, "incorrect"))
        self.assertEqual(
            evidence.result_errors(
                self.receipt("Wrong answer", 1, [{"Number": 2}]), 3, "incorrect"
            ),
            [],
        )

    def test_boolean_counts_are_not_integer_acceptance(self):
        row = self.receipt(passed=True)
        row["result"]["Total"] = True
        self.assertTrue(evidence.result_errors(row, 1, "solution"))

    def test_prepare_matches_explicit_csharp_cpp_and_java_contracts(self):
        entry = {
            "prefix": "support",
            "suffix": "tail",
            "filename": "Answer.cs",
            "language": "csharp",
        }
        self.assertEqual(
            evidence.compose(entry, "body"),
            'support\n#line 1 "Answer.cs"\nbody\n#line default\ntail',
        )
        entry.update(language="cpp", filename="answer.cc")
        self.assertEqual(
            evidence.compose(entry, "body"),
            'support\n#line 1 "answer.cc"\nbody\n#line 1 "bank-support.cpp"\ntail',
        )
        entry.update(language="java", filename="Answer.java")
        self.assertEqual(evidence.compose(entry, "body"), "support\nbody\ntail")
        entry.update(language="javascript", filename="solution.js")
        self.assertEqual(
            evidence.compose(entry, "body"), "support\n(() => {\nbody\ntail\n})();\n"
        )
        entry.update(language="python", filename="solution.py")
        self.assertEqual(
            evidence.compose(entry, "x=1"),
            "support\n\nexec(compile(__import__('base64').b64decode('eD0x'), 'solution.py', 'exec'), globals())\ntail",
        )

    def test_java_import_hoist_preserves_utf16_lines_and_only_leading_directives(self):
        source = (
            "// comment\nimport /* 🌱 */ java.util.List;\nint run() { return 0; }\n"
        )
        body, imports = evidence.java_imports(source)
        self.assertEqual(imports, "import /* 🌱 */ java.util.List;\n")
        self.assertEqual(body.count("\n"), source.count("\n"))
        self.assertEqual(len(body.encode("utf-16-le")), len(source.encode("utf-16-le")))
        self.assertTrue(body.startswith("// comment\n"))
        self.assertTrue(body.endswith("int run() { return 0; }\n"))
        entry = {
            "prefix": "package epi;\nclass Answer {\n",
            "suffix": "}\n",
            "filename": "Answer.java",
            "language": "java",
        }
        prepared = evidence.compose(entry, source)
        self.assertTrue(
            prepared.startswith("package epi;\n" + imports + "\nclass Answer {\n")
        )
        for code in (
            'String x = "import fake.Type;";',
            "important();",
            "/* unfinished import x.Y;",
        ):
            self.assertEqual(evidence.java_imports(code), (code, ""))

    def test_metadata_exceptions_never_ignore_other_runtime_files_or_omissions(self):
        current = {
            "runner.cs": "A" * 64,
            "workspace-code/catalog.json": "B" * 64,
            "EpiJudge.Runner/CallableCodeCatalog.cs": "C" * 64,
        }
        old_metadata = dict(
            current,
            **{
                "workspace-code/catalog.json": "D" * 64,
                "EpiJudge.Runner/CallableCodeCatalog.cs": "E" * 64,
            },
        )
        self.assertFalse(evidence.same_runtime_sources(old_metadata, current))
        self.assertTrue(
            evidence.same_runtime_sources(
                old_metadata, current, allow_entry_local_metadata=True
            )
        )
        self.assertFalse(
            evidence.same_runtime_sources(
                {**old_metadata, "runner.cs": "F" * 64},
                current,
                allow_entry_local_metadata=True,
            )
        )
        self.assertFalse(
            evidence.same_runtime_sources(
                {"runner.cs": "A" * 64}, current, allow_entry_local_metadata=True
            )
        )

    def test_unchanged_program_reuses_metadata_but_old_changed_program_cannot_override(
        self,
    ):
        with tempfile.TemporaryDirectory(
            prefix="callable-incremental-evidence-"
        ) as temporary:
            root = Path(temporary)
            (root / ".epi-runs").mkdir()
            key = ("p", "java", "solution")
            current = {
                "runner.cs": "A" * 64,
                "workspace-code/catalog.json": "B" * 64,
                "EpiJudge.Runner/CallableCodeCatalog.cs": "C" * 64,
            }
            old_metadata = {
                **current,
                "workspace-code/catalog.json": "D" * 64,
                "EpiJudge.Runner/CallableCodeCatalog.cs": "E" * 64,
            }
            target = {
                "collection": "epi",
                "testCount": 3,
                **{
                    name: "A" * 64
                    for name in (
                        "codeSha256",
                        "composedCodeSha256",
                        "notesSha256",
                        "corpusSha256",
                        "harnessSha256",
                    )
                },
            }
            row = {
                "problemId": "p",
                "language": "java",
                "role": "solution",
                "collection": "epi",
                "displayedEmbeddedCode": True,
                "codeFormat": "callable-v1",
                **self.receipt(),
                **{
                    name: value
                    for name, value in target.items()
                    if name.endswith("Sha256")
                },
            }

            def save(name, source, execution, stamp):
                path = root / ".epi-runs" / f"solutions-audit-callable-{name}.json"
                path.write_text(
                    json.dumps({"sourceHashes": source, "executions": [execution]}),
                    encoding="utf-8",
                )
                os.utime(path, ns=(stamp, stamp))

            save("unchanged-pass", old_metadata, row, 100)
            accepted, _ = evidence.matrix_evidence(root, {key: target}, current)
            self.assertEqual(len(accepted), 1)
            old_failure = copy.deepcopy(row)
            old_failure.update(success=False, composedCodeSha256="F" * 64)
            save("old-program-failure", old_metadata, old_failure, 200)
            accepted, _ = evidence.matrix_evidence(root, {key: target}, current)
            self.assertEqual(len(accepted), 1)
            # A genuine later failure of the identical current program still
            # invalidates acceptance, even when its metadata snapshot is older.
            current_program_failure = copy.deepcopy(row)
            current_program_failure["success"] = False
            save("current-program-failure", old_metadata, current_program_failure, 300)
            with self.assertRaisesRegex(
                evidence.EvidenceError, "current-program-failure"
            ):
                evidence.matrix_evidence(root, {key: target}, current)

    def test_wrong_body_hash_invalidates_older_pass_even_with_current_runtime(self):
        with tempfile.TemporaryDirectory(prefix="callable-body-evidence-") as temporary:
            root = Path(temporary)
            (root / ".epi-runs").mkdir()
            key = ("p", "java", "solution")
            target = {
                "collection": "epi",
                "testCount": 3,
                **{
                    name: "A" * 64
                    for name in (
                        "codeSha256",
                        "composedCodeSha256",
                        "notesSha256",
                        "corpusSha256",
                        "harnessSha256",
                    )
                },
            }
            row = {
                "problemId": "p",
                "language": "java",
                "role": "solution",
                "collection": "epi",
                "displayedEmbeddedCode": True,
                "codeFormat": "callable-v1",
                **self.receipt(),
                **{
                    name: value
                    for name, value in target.items()
                    if name.endswith("Sha256")
                },
            }
            for index, body_hash in enumerate(("A" * 64, "B" * 64)):
                current_row = copy.deepcopy(row)
                current_row["codeSha256"] = body_hash
                path = root / ".epi-runs" / f"solutions-audit-callable-{index}.json"
                path.write_text(
                    json.dumps(
                        {
                            "sourceHashes": {"runner.cs": "C" * 64},
                            "executions": [current_row],
                        }
                    ),
                    encoding="utf-8",
                )
                os.utime(path, ns=(100 + index, 100 + index))
            with self.assertRaisesRegex(
                evidence.EvidenceError, "codeSha256 is stale/mismatched"
            ):
                evidence.matrix_evidence(root, {key: target}, {"runner.cs": "C" * 64})

    def test_failed_aggregation_does_not_write_or_replace_acceptance(self):
        with tempfile.TemporaryDirectory(
            prefix="callable-acceptance-write-"
        ) as temporary:
            output = Path(temporary) / "validation-results.json"
            output.write_text("previous complete evidence\n", encoding="utf-8")
            with (
                patch.object(
                    evidence,
                    "accept",
                    side_effect=evidence.EvidenceError("missing starter"),
                ),
                patch("sys.argv", ["evidence.py", "--output", str(output)]),
                redirect_stdout(io.StringIO()),
            ):
                self.assertEqual(evidence.main(), 1)
            self.assertEqual(
                output.read_text(encoding="utf-8"), "previous complete evidence\n"
            )

    def test_archived_rows_cannot_be_omitted_or_only_claimed(self):
        with tempfile.TemporaryDirectory(prefix="callable-raw-evidence-") as temporary:
            archive = Path(temporary) / "executed.json"
            raw = [
                {"Actual": n, "Error": None, "ValidationFailed": False}
                for n in range(3)
            ]
            archive.write_text(json.dumps(raw), encoding="utf-8")
            row = {
                "executionReportRows": 3,
                "executionReportSha256": evidence.file_sha(archive),
            }
            self.assertEqual(evidence.archive_errors(archive, row, 3, "correct"), [])
            archive.write_text(json.dumps(raw[:2]), encoding="utf-8")
            # Even a fresh checksum and a claimed complete count cannot hide
            # the missing actual execution row.
            row["executionReportSha256"] = evidence.file_sha(archive)
            self.assertIn(
                "raw execution archive omitted corpus rows",
                evidence.archive_errors(archive, row, 3, "correct"),
            )

    def test_archive_errors_and_structural_failures_contradict_correct_claim(self):
        with tempfile.TemporaryDirectory(prefix="callable-raw-structure-") as temporary:
            archive = Path(temporary) / "executed.json"
            for raw in (
                [{"Error": None}],
                [{"Actual": 1, "ValidationFailed": True}],
                [{"Actual": 1, "Error": "node identity changed"}],
            ):
                with self.subTest(raw=raw):
                    archive.write_text(json.dumps(raw), encoding="utf-8")
                    row = {
                        "executionReportRows": 1,
                        "executionReportSha256": evidence.file_sha(archive),
                    }
                    self.assertTrue(evidence.archive_errors(archive, row, 1, "correct"))

    def test_missing_or_replaced_archive_is_rejected(self):
        with tempfile.TemporaryDirectory(prefix="callable-raw-checksum-") as temporary:
            archive = Path(temporary) / "executed.json"
            row = {"executionReportRows": 1, "executionReportSha256": "A" * 64}
            self.assertIn(
                "raw execution archive is missing",
                evidence.archive_errors(archive, row, 1, "correct"),
            )
            archive.write_text('[{"Actual": 1}]', encoding="utf-8")
            self.assertIn(
                "raw execution archive checksum differs",
                evidence.archive_errors(archive, row, 1, "correct"),
            )


if __name__ == "__main__":
    unittest.main()


class CtciInventoryExtensionTests(unittest.TestCase):
    def test_original_counts_remain_required_without_ctci_snapshot(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(
                {"epi": 218, "blind75": 75, "interviewcake": 41},
                evidence.expected_collections(Path(directory)),
            )

    def test_ctci_count_comes_from_unique_valid_reviewed_snapshot_ids(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "ctci6").mkdir()
            rows = [
                {"id": "ctci6_1_1", "collection": "ctci6"},
                {"id": "ctci6_8_11", "collection": "ctci6"},
            ]
            (root / "ctci6/catalog.json").write_text(json.dumps(rows))
            self.assertEqual(2, evidence.expected_collections(root)["ctci6"])
            for invalid in (
                rows + [rows[0]],
                [{"id": "ctci6_bad", "collection": "ctci6"}],
                [{"id": "ctci6_1_1", "collection": "epi"}],
                [],
            ):
                (root / "ctci6/catalog.json").write_text(json.dumps(invalid))
                with self.assertRaises(evidence.EvidenceError):
                    evidence.expected_collections(root)
