"""Regression checks for isolated callable-source boundaries and dependencies."""

from __future__ import annotations

import ast
import json
import unittest

from common import ROOT, parse
from isolated import (
    BLIND_MODELS,
    CAKE_MODELS,
    helper_name,
    literal_assignment,
    prune_probe,
    references_for,
    required_models,
    split,
    support_envelope,
    support_prefix,
    ts_calls,
    ts_name,
)


class IsolatedSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.blind = json.loads(
            (ROOT / "blind75/catalog.json").read_text(encoding="utf-8")
        )
        cls.cake = json.loads(
            (ROOT / "interviewcake/catalog.json").read_text(encoding="utf-8")
        )
        cls.headers = {
            "blind75": literal_assignment(
                ROOT / "scripts/blind75/generate.py", "HEADERS"
            ),
            "interviewcake": literal_assignment(
                ROOT / "scripts/interviewcake/banktypes.py", "HEADER"
            ),
        }

    def cleaned(self, problem: str, language: str):
        extension = {
            "csharp": "cs",
            "javascript": "js",
            "python": "py",
            "cpp": "cpp",
            "java": "java",
        }[language]
        spec = next(r for r in self.blind + self.cake if r["id"] == problem)
        collection = "blind75" if problem.startswith("blind75_") else "interviewcake"
        models = BLIND_MODELS if collection == "blind75" else CAKE_MODELS
        source = (
            ROOT / "solutions" / language / (problem + "." + extension)
        ).read_text(encoding="utf-8")
        return split(source, language, models, helper_name(spec, collection))

    def test_primitive_starters_need_no_supplied_type_reference(self):
        for collection, rows in (("blind75", self.blind), ("interviewcake", self.cake)):
            empty = [r for r in rows if not required_models(r, collection)]
            self.assertEqual(len(empty), 57 if collection == "blind75" else 26)
        apple = next(r for r in self.cake if r["sourceId"] == "stock-price")
        self.assertEqual(required_models(apple, "interviewcake"), [])

    def test_unknown_initialization_is_rejected_instead_of_dropped(self):
        with self.assertRaises(AssertionError):
            split(
                "initialize_state()\n\ndef answer():\n    return 1\n",
                "python",
                (),
                "Unused",
            )

    def test_cs_java_models_follow_user_imports_and_callable_code(self):
        bodies = {
            "csharp": "using System.Numerics;\npublic class Solution { public static int F() { return (int)BigInteger.One; } }\n",
            "java": "import java.math.BigInteger;\nclass Solution { public static int f() { return BigInteger.ONE.intValueExact(); } }\n",
        }
        for collection, models in (
            ("blind75", BLIND_MODELS),
            ("interviewcake", CAKE_MODELS),
        ):
            for language, body in bodies.items():
                with self.subTest(collection=collection, language=language):
                    prefix, suffix = support_envelope(
                        self.headers[collection][language], [], language, models
                    )
                    prefix_names = {
                        ts_name(node, prefix)
                        for node in parse(prefix, language).root_node.named_children
                    }
                    suffix_names = {
                        ts_name(node, suffix)
                        for node in parse(suffix, language).root_node.named_children
                    }
                    self.assertFalse(set(models) & prefix_names)
                    self.assertTrue(set(models) <= suffix_names)
                    self.assertFalse(
                        parse(prefix + body + suffix, language).root_node.has_error
                    )

    def test_two_sum_has_no_hidden_algorithm_library(self):
        for language in ("javascript", "python", "cpp", "java"):
            with self.subTest(language=language):
                code, imports, _, removed = self.cleaned("blind75_two_sum", language)
                self.assertNotIn("Probe", code)
                self.assertNotIn("TreeAlgorithms", code)
                self.assertNotIn("component_count", code)
                self.assertNotIn("word_exists", code)
                prefix = support_prefix(
                    self.headers["blind75"][language], imports, language, BLIND_MODELS
                )
                self.assertNotIn("Probe", prefix + code)
                self.assertTrue(removed)

    def test_transitive_tree_helpers_remain_visible(self):
        for language in ("javascript", "python", "cpp", "java"):
            with self.subTest(language=language):
                code, _, symbols, removed = self.cleaned(
                    "blind75_subtree_of_another_tree", language
                )
                self.assertIn("TreeAlgorithms.same", symbols)
                self.assertIn("TreeAlgorithms.subtree", symbols)
                self.assertIn("Probe.depth", removed)
                self.assertNotIn("Probe.same", removed)
                self.assertNotIn("Probe", code)

    def test_cpp_nested_dependencies_and_order(self):
        code, _, symbols, _ = self.cleaned(
            "blind75_binary_tree_maximum_path_sum", "cpp"
        )
        self.assertIn("TreeAlgorithms.gain", symbols)
        self.assertIn("TreeAlgorithms.maxPath", symbols)
        self.assertLess(
            code.index("namespace TreeAlgorithms"), code.index("class Solution")
        )
        self.assertFalse(parse(code, "cpp").root_node.has_error)

    def test_java_overloaded_algorithm_helpers_are_retained(self):
        code, _, symbols, _ = self.cleaned("blind75_clone_graph", "java")
        self.assertEqual(code.count("static Node clone("), 2)
        self.assertIn("GraphAlgorithms.clone", symbols)
        self.assertNotIn("static int depth", code)

    def test_merge_k_callback_dependency_is_not_pruned(self):
        for language in ("javascript", "python", "cpp", "java"):
            with self.subTest(language=language):
                code, _, symbols, removed = self.cleaned(
                    "blind75_merge_k_sorted_lists", language
                )
                self.assertIn("ListAlgorithms.nodes", symbols)
                self.assertIn("ListAlgorithms.link", symbols)
                self.assertNotIn("Probe.nodes", removed)
                self.assertNotIn("ListAlgorithms.depth", symbols)
                self.assertIn("ListAlgorithms", code)

    def test_callback_dependencies_are_transitive(self):
        source = """
const Probe = {
    nodes(value) { return [value].flatMap(this.expand); },
    expand(value) { return [value]; },
    unrelated(value) { return value; }
};
"""
        container = parse(source, "javascript").root_node.named_children[0]
        code, symbols, removed = prune_probe(
            container,
            source,
            "javascript",
            "function merge(lists) { return lists.flatMap(Probe.nodes); }",
            "ListAlgorithms",
        )
        self.assertIn("ListAlgorithms.nodes", symbols)
        self.assertIn("ListAlgorithms.expand", symbols)
        self.assertIn("Probe.unrelated", removed)
        self.assertNotIn("unrelated", code)

    def test_native_method_references_are_dependencies(self):
        self.assertEqual(
            ts_calls(
                "class Example { void f() { stream.map(Probe::nodes); } }",
                "java",
                external=True,
            ),
            {"nodes"},
        )
        self.assertEqual(
            ts_calls(
                "void f() { auto callback = Probe::nodes; }", "cpp", external=True
            ),
            {"nodes"},
        )

    def test_python_shared_helpers_only_when_called(self):
        code, _, symbols, removed = self.cleaned("blind75_word_search", "python")
        self.assertIn("word_exists", symbols)
        self.assertNotIn("component_count", symbols)
        self.assertIn("component_count", removed)
        self.assertEqual(
            {n.name for n in ast.parse(code).body if isinstance(n, ast.FunctionDef)},
            {"exist", "word_exists"},
        )

    def test_random_reference_shows_only_permitted_primitive(self):
        for mode, method in (
            ("shuffle", "GetRandom"),
            ("rand5", "Rand7"),
            ("rand7", "Rand5"),
        ):
            spec = next(r for r in self.cake if r["mode"] == mode)
            for language in ("csharp", "javascript", "python", "cpp", "java"):
                with self.subTest(mode=mode, language=language):
                    references = references_for(
                        spec,
                        "interviewcake",
                        language,
                        self.headers["interviewcake"][language],
                    )
                    self.assertEqual(len(references), 1)
                    code = references[0]["code"]
                    self.assertIn(method + "(", code)
                    self.assertNotIn("Draw", code)
                    self.assertNotIn("LinkedListNode", code)

    def test_stateful_task_class_remains_editable(self):
        for problem, expected in (
            ("blind75_implement_trie_prefix_tree", "Trie"),
            ("interviewcake_temperature-tracker", "TempTracker"),
        ):
            for language in ("csharp", "javascript", "python", "cpp", "java"):
                with self.subTest(problem=problem, language=language):
                    code, _, symbols, _ = self.cleaned(problem, language)
                    self.assertIn(expected, symbols)
                    self.assertIn("class " + expected, code)


if __name__ == "__main__":
    unittest.main()
