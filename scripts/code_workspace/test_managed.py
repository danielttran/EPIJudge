"""Whole-inventory checks for the independently generated managed code part."""

import ast
import hashlib
import json
import sys
import unittest
from collections import Counter
from itertools import pairwise
from unittest.mock import patch

from common import ROOT, parse, text_of
from managed import parser_errors, problems, python_dependencies


class ManagedWorkspaceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.part = json.loads(
            (ROOT / "workspace-code/parts/epi-managed.json").read_text(encoding="utf-8")
        )
        cls.entries = cls.part["entries"]
        cls.roots = json.loads(
            (ROOT / "scripts/code_workspace/managed-roots.json").read_text(encoding="utf-8")
        )["roots"]
        cls.problems = {p["Id"]: p for p in problems()}
        sys.path.insert(0, str(ROOT / "epi_judge_python"))

    def test_exact_live_inventory(self):
        self.assertEqual(self.part["schemaVersion"], 1)
        self.assertEqual(self.part["codeFormat"], "callable-v1")
        self.assertEqual(
            Counter(e["language"] for e in self.entries),
            {"csharp": 218, "javascript": 218, "python": 218},
        )
        self.assertEqual(len({(e["problemId"], e["language"]) for e in self.entries}), 654)
        self.assertEqual({e["problemId"] for e in self.entries}, set(self.roots))

    def test_annotation_dependencies_do_not_require_symtable_annotation_reporting(self):
        code = (
            "from typing import List, Set\n"
            "class GraphVertex:\n"
            "    def __init__(self):\n"
            "        self.edges: List[GraphVertex] = []\n"
            "def algorithm(value):\n"
            "    seen: Set[int] = set()\n"
            "    def helper(items: List[int]) -> Set[int]:\n"
            "        return set(items)\n"
            "    return helper(value)\n"
        )
        definitions = {
            node.name: node
            for node in ast.parse(code).body
            if isinstance(node, (ast.ClassDef, ast.FunctionDef))
        }
        # Reproduce Python 3.14's omission of annotation-only symtable loads.
        with patch("managed.referenced_globals", return_value=set()):
            dependencies = python_dependencies(code, definitions)
        self.assertTrue({"List", "GraphVertex"} <= dependencies["GraphVertex"])
        self.assertTrue({"List", "Set"} <= dependencies["algorithm"])

    def test_original_sources_are_fingerprinted(self):
        for entry in self.entries:
            with self.subTest(problem=entry["problemId"], language=entry["language"]):
                problem = self.problems[entry["problemId"]]
                starter_key = {
                    "csharp": "StarterCode",
                    "javascript": "JsStarterCode",
                    "python": "PyStarterCode",
                }[entry["language"]]
                original_solution = ROOT / entry["sourcePaths"][1]
                for key, code in (
                    ("starter", problem[starter_key]),
                    ("solution", original_solution.read_text(encoding="utf-8")),
                ):
                    self.assertEqual(
                        hashlib.sha256(code.encode("utf-8")).hexdigest(), entry["sourceSha256"][key]
                    )

    def test_python_algorithms_and_starters_keep_original_ast(self):
        for entry in self.entries:
            if entry["language"] != "python":
                continue
            original_solution = (ROOT / entry["sourcePaths"][1]).read_text(encoding="utf-8")
            roots = self.roots[entry["problemId"]]
            for kind, original in (
                ("starterCode", self.problems[entry["problemId"]]["PyStarterCode"]),
                ("solutionCode", original_solution),
            ):
                original_defs = {
                    n.name: n
                    for n in ast.parse(original).body
                    if isinstance(n, (ast.FunctionDef, ast.ClassDef))
                }
                visible_defs = {
                    n.name: n
                    for n in ast.parse(entry[kind]).body
                    if isinstance(n, (ast.FunctionDef, ast.ClassDef))
                }
                with self.subTest(problem=entry["problemId"], kind=kind):
                    self.assertTrue(set(roots) <= visible_defs.keys())
                    for name, definition in visible_defs.items():
                        self.assertEqual(
                            ast.dump(definition, include_attributes=False),
                            ast.dump(original_defs[name], include_attributes=False),
                        )

    def test_all_436_python_programs_initialize(self):
        count = 0
        for entry in self.entries:
            if entry["language"] != "python":
                continue
            for kind in ("starterCode", "solutionCode"):
                with self.subTest(problem=entry["problemId"], kind=kind):
                    namespace = {"__name__": "solution", "__file__": "solution.py"}
                    program = entry["prefix"] + entry[kind] + entry["suffix"]
                    # Only trusted, checked-in bank fixtures are executed here.
                    exec(compile(program, "solution.py", "exec"), namespace)  # noqa: S102
                    for root in self.roots[entry["problemId"]]:
                        self.assertTrue(callable(namespace[root]))
                    count += 1
        self.assertEqual(count, 436)

    def test_python_glue_and_models_are_not_editable(self):
        forbidden = {"TestFailure", "enable_executor_hook", "generic_test", "run_func_with_retries"}
        for entry in self.entries:
            if entry["language"] != "python":
                continue
            roots = set(self.roots[entry["problemId"]])
            hidden_definitions = {
                n.name
                for n in ast.parse(entry["prefix"]).body
                if isinstance(n, (ast.FunctionDef, ast.ClassDef))
            }
            self.assertFalse(roots & hidden_definitions)
            model_names = {name for reference in entry["references"] for name in reference["names"]}
            for kind in ("starterCode", "solutionCode"):
                tree = ast.parse(entry[kind])
                with self.subTest(problem=entry["problemId"], kind=kind):
                    self.assertFalse(
                        any(
                            isinstance(n, ast.ImportFrom)
                            and (n.module or "").startswith("test_framework")
                            for n in tree.body
                        )
                    )
                    self.assertFalse(
                        {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)} & forbidden
                    )
                    self.assertFalse(
                        any(
                            isinstance(n, ast.If)
                            and any(
                                isinstance(v, ast.Name) and v.id == "__name__"
                                for v in ast.walk(n.test)
                            )
                            for n in tree.body
                        )
                    )
                    visible_types = {n.name for n in tree.body if isinstance(n, ast.ClassDef)}
                    self.assertFalse((visible_types - roots) & model_names)

    def test_all_872_csharp_javascript_artifacts_parse(self):
        count = 0
        for entry in self.entries:
            if entry["language"] not in {"csharp", "javascript"}:
                continue
            for kind in ("starterCode", "solutionCode"):
                source = entry[kind]
                with self.subTest(
                    problem=entry["problemId"], language=entry["language"], kind=kind
                ):
                    errors = parser_errors(source, entry["language"])
                    if errors:
                        self.assertEqual(
                            (entry["problemId"], entry["language"], kind, errors),
                            (
                                "string_decompositions_into_dictionary_words",
                                "csharp",
                                "solutionCode",
                                ["required"],
                            ),
                        )
                    if entry["language"] == "javascript":
                        self.assertNotIn("module.exports", source)
                        self.assertIn("module.exports", entry["suffix"])
                    else:
                        self.assertNotIn("EpiJudge.TestFramework", source)
                        self.assertNotIn("static void Main", source)
                        classes = [
                            n
                            for n in parse(source, "csharp").root_node.named_children
                            if n.type == "class_declaration"
                        ]
                        self.assertEqual(
                            [text_of(n.child_by_field_name("name"), source) for n in classes],
                            ["Solution"],
                        )
                    count += 1
        self.assertEqual(count, 872)

    def test_csharp_algorithm_tokens_are_preserved(self):
        def class_tokens(source):
            declaration = next(
                node
                for node in parse(source, "csharp").root_node.named_children
                if node.type == "class_declaration"
            )

            def leaves(node):
                if node.type == "comment":
                    return []
                if not node.children:
                    return [(node.type, text_of(node, source))]
                return [token for child in node.children for token in leaves(child)]

            return leaves(declaration)

        for entry in self.entries:
            if entry["language"] != "csharp":
                continue
            originals = {
                "starterCode": self.problems[entry["problemId"]]["StarterCode"],
                "solutionCode": (ROOT / entry["sourcePaths"][1]).read_text(encoding="utf-8"),
            }
            for kind, original in originals.items():
                with self.subTest(problem=entry["problemId"], kind=kind):
                    self.assertEqual(class_tokens(original), class_tokens(entry[kind]))

    def test_references_only_expose_required_names(self):
        for entry in self.entries:
            source = entry["starterCode"] + entry["solutionCode"]
            names = [name for reference in entry["references"] for name in reference["names"]]
            with self.subTest(problem=entry["problemId"], language=entry["language"]):
                self.assertEqual(len(names), len(set(names)))
                self.assertTrue(all(name in source for name in names))
                self.assertTrue(all(reference["code"].strip() for reference in entry["references"]))

    def test_stateful_structural_and_boundary_algorithms(self):
        entries = {e["problemId"]: e for e in self.entries if e["language"] == "python"}

        def load(problem_id):
            entry = entries[problem_id]
            namespace = {"__name__": "solution", "__file__": "solution.py"}
            # The contract smoke executes trusted generated bank algorithms.
            exec(  # noqa: S102
                compile(
                    entry["prefix"] + entry["solutionCode"] + entry["suffix"], "solution.py", "exec"
                ),
                namespace,
            )
            return namespace

        rotate = load("rotate_array")["rotate_array"]
        values = [1, 2, 3]
        rotate(-1, values)
        self.assertEqual(values, [2, 3, 1])
        rotate(20, [])

        namespace = load("graph_clone")
        node = namespace["GraphVertex"](7)
        node.edges.append(node)
        clone = namespace["clone_graph"](node)
        self.assertIsNot(clone, node)
        self.assertIs(clone.edges[0], clone)

        queue_type = load("queue_from_stacks")["Queue"]
        queue = queue_type()
        queue.enqueue(1)
        queue.enqueue(2)
        self.assertEqual(queue.dequeue(), 1)
        self.assertEqual(queue.dequeue(), 2)
        self.assertRaises(IndexError, queue.dequeue)

        credit_type = load("adding_credits")["ClientsCreditsInfo"]
        credit = credit_type()
        credit.insert("first", 3)
        credit.add_all(10)
        self.assertEqual(credit.lookup("first"), 13)
        self.assertEqual(credit.max(), "first")
        self.assertEqual(credit_type().max(), "")

        random = load("uniform_random_number")["uniform_random"]
        self.assertEqual(random(-(2**31), -(2**31)), -(2**31))
        self.assertTrue(all(-(2**31) <= random(-(2**31), 2**31 - 1) < 2**31 for _ in range(100)))

        gray = load("gray_code")
        self.assertIn("differ_by_1_bit", entries["gray_code"]["hiddenSymbols"])
        values = gray["gray_code"](5)
        self.assertEqual(len(set(values)), 32)
        self.assertTrue(
            all(gray["differ_by_1_bit"](left, right) for left, right in pairwise(values))
        )
        self.assertFalse(gray["differ_by_1_bit"](0, 3))


if __name__ == "__main__":
    unittest.main()
