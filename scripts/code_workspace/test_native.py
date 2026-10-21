"""Native callable boundary tests across the complete218-question inventory."""

import hashlib
import json
import unittest

try:
    from .common import ROOT, parse
    from .native import annotation_names, identifiers, name_of, selfcheck, walk
except ImportError:
    from common import ROOT, parse
    from native import annotation_names, identifiers, name_of, selfcheck, walk


class NativeWorkspaceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.entries = json.loads(
            (ROOT / "workspace-code/parts/epi-native.json").read_text(encoding="utf-8")
        )["entries"]
        cls.by_key = {(e["problemId"], e["language"]): e for e in cls.entries}

    def test_complete_native_inventory(self):
        self.assertEqual(len(self.entries), 436)
        self.assertEqual(len(self.by_key), 436)
        for language in ("cpp", "java"):
            self.assertEqual(sum(e["language"] == language for e in self.entries), 218)

    def test_every_visible_and_composed_artifact(self):
        for entry in self.entries:
            with self.subTest(problem=entry["problemId"], language=entry["language"]):
                selfcheck(entry)

    def test_every_owned_source_fingerprint(self):
        for entry in self.entries:
            for kind, path in zip(("starter", "solution"), entry["sourcePaths"][:2]):
                with self.subTest(
                    problem=entry["problemId"], language=entry["language"], kind=kind
                ):
                    self.assertEqual(
                        hashlib.sha256((ROOT / path).read_bytes()).hexdigest(),
                        entry["sourceSha256"][kind],
                    )

    def test_starters_have_no_algorithm_implementation(self):
        for entry in self.entries:
            code = entry["starterCode"]
            if entry["language"] == "java":
                code = "class __Visible {\n" + code + "\n}"
            tree = parse(code, entry["language"])
            for node in walk(tree.root_node):
                if node.type in {
                    "function_definition",
                    "method_declaration",
                    "constructor_declaration",
                }:
                    body = node.child_by_field_name("body")
                    with self.subTest(
                        problem=entry["problemId"],
                        language=entry["language"],
                        line=node.start_point.row,
                    ):
                        statements = [
                            n
                            for n in body.named_children
                            if n.type
                            not in {"comment", "line_comment", "block_comment"}
                        ]
                        self.assertEqual(
                            [n.type for n in statements], ["throw_statement"]
                        )

    def test_checker_helpers_are_independent(self):
        cases = [
            ("cpp", "gray_code", "DiffersByOneBit"),
            ("java", "gray_code", "differsByOneBit"),
            ("java", "do_lists_overlap", "nodes"),
        ]
        for language, problem, name in cases:
            entry = self.by_key[(problem, language)]
            self.assertIn("__bank_" + name, entry["suffix"])
            self.assertIn(name, entry["solutionCode"])
            self.assertNotIn("__bank_" + name, entry["solutionCode"])
            self.assertNotIn(name, entry["starterCode"])

    def test_cpp_starters_retain_signature_required_type_aliases(self):
        for entry in self.entries:
            if entry["language"] != "cpp":
                continue
            solution = entry["solutionCode"]
            starter = entry["starterCode"]
            aliases = {
                name_of(n, solution): n
                for n in parse(solution, "cpp").root_node.named_children
                if n.type in {"alias_declaration", "type_definition"}
            }
            starter_tree = parse(starter, "cpp")
            required = identifiers(starter_tree.root_node, starter) & aliases.keys()
            declared = {
                name_of(n, starter)
                for n in starter_tree.root_node.named_children
                if n.type in {"alias_declaration", "type_definition"}
            }
            with self.subTest(problem=entry["problemId"]):
                self.assertTrue(required <= declared)
        skyline = self.by_key[("drawing_skyline", "cpp")]["starterCode"]
        self.assertIn("using Skyline = vector<Rect>;", skyline)
        self.assertIn("Skyline ComputeSkyline", skyline)

    def test_only_required_external_model_references(self):
        simple = self.by_key[("two_sum", "cpp")]
        self.assertEqual(simple["references"], [])
        for language in ("cpp", "java"):
            linked = self.by_key[("reverse_list", language)]
            self.assertTrue(
                any("ListNode" in ref["names"] for ref in linked["references"])
            )
            for ref in linked["references"]:
                self.assertNotIn("SerializationTrait", ref["code"])
                self.assertNotIn("GenericTest", ref["code"])
                self.assertNotIn("toString", ref["code"])

    def test_java_annotations_live_only_in_hidden_adapter(self):
        for problem in ("count_bits", "two_sum", "rectangle_intersection"):
            entry = self.by_key[(problem, "java")]
            self.assertNotIn("@EpiTest", entry["solutionCode"])
            self.assertIn("@EpiTest", entry["suffix"])
            self.assertIn("__bankCase", entry["suffix"])

    def test_every_java_reflection_comparator_survives_with_unchanged_tokens(self):
        def callbacks(source):
            tree = parse(source, "java")
            result = {}
            for node in walk(tree.root_node):
                if (
                    node.type == "method_declaration"
                    and "EpiTestComparator" in annotation_names(node, source)
                ):
                    tokens = [
                        (n.type, source.encode("utf-8")[n.start_byte : n.end_byte])
                        for n in walk(node)
                        if not n.children
                        and n.type not in {"line_comment", "block_comment"}
                    ]
                    result[name_of(node, source)] = tokens
            return result

        total = 0
        for entry in self.entries:
            if entry["language"] != "java":
                continue
            source = (ROOT / entry["sourcePaths"][1]).read_text(encoding="utf-8")
            expected = callbacks(source)
            actual = callbacks(
                entry["prefix"] + entry["solutionCode"] + entry["suffix"]
            )
            with self.subTest(problem=entry["problemId"]):
                self.assertEqual(expected, actual)
            total += len(expected)
        self.assertGreater(total, 0)


if __name__ == "__main__":
    unittest.main()
