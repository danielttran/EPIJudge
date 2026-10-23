"""Adversarial presentation fixtures: execution success alone is insufficient."""

import copy
import unittest
from unittest.mock import patch

from audit import (
    audit_artifact,
    audit_envelope,
    audit_references,
    helper_dependencies,
    isolated_global_dependencies,
)
from common import format_code


def entry(code, language="csharp", problem_id="interviewcake_stock-price"):
    return {
        "problemId": problem_id,
        "language": language,
        "filename": "solution",
        "signature": "method",
        "starterCode": code,
        "solutionCode": code,
        "prefix": "",
        "suffix": "",
        "references": [],
        "visibleSymbols": ["Solution"],
        "hiddenSymbols": [],
    }


class CallableContentGateTests(unittest.TestCase):
    def test_apple_stocks_rejects_unrelated_supplied_model_even_if_manifest_claims_it(
        self,
    ):
        code = format_code(
            "public class LinkedListNode { public int Value; }\npublic class Solution { public int GetMaxProfit(int[] p) { return p[1]-p[0]; } }",
            "csharp",
        )
        fixture = entry(code)
        fixture["visibleSymbols"].append("LinkedListNode")
        result = audit_artifact(fixture, "solution")
        self.assertFalse(result["success"])
        self.assertTrue(
            any("Bank-supplied models" in error for error in result["errors"])
        )

    def test_clean_callable_and_related_algorithm_class_are_allowed(self):
        code = format_code(
            "public class Solution { private sealed class Heap { public int Value; } public int Run(int n) { var heap = new Heap(); heap.Value=n; return heap.Value; } }",
            "csharp",
        )
        self.assertTrue(audit_artifact(entry(code), "solution")["success"])

    def test_program_main_and_framework_call_are_rejected(self):
        code = format_code(
            "int CountBits(unsigned x) { return x; } int main(int argc,char** argv) { return GenericTestMain(argc,argv); }",
            "cpp",
        )
        result = audit_artifact(entry(code, "cpp"), "solution")
        self.assertFalse(result["success"])
        self.assertTrue(any("main entry" in error for error in result["errors"]))
        self.assertTrue(any("GenericTestMain" in error for error in result["errors"]))

    def test_python_decorator_and_framework_import_are_rejected(self):
        code = "from test_framework import generic_test\n\n\n@enable_executor_hook\ndef run(x):\n    return x\n"
        result = audit_artifact(entry(code, "python"), "solution", check_format=False)
        self.assertFalse(result["success"])
        self.assertTrue(
            any("Judge-framework imports" in error for error in result["errors"])
        )

    def test_export_glue_is_rejected(self):
        code = format_code(
            "function run(x) { return x; }\nmodule.exports = {run};", "javascript"
        )
        result = audit_artifact(entry(code, "javascript"), "solution")
        self.assertFalse(result["success"])
        self.assertIn("JavaScript export glue is visible", result["errors"])

    def test_unused_probe_library_is_rejected(self):
        code = "function twoSum(a) { return a; }\nconst Probe = { same(a,b) { return a===b; }, invert(x) { return x; } };\n"
        errors, decisions = helper_dependencies(code, "javascript")
        self.assertTrue(errors)
        self.assertEqual(decisions[0]["entryCalls"], [])

    def test_unused_library_cannot_be_moved_into_hidden_support(self):
        fixture = entry(
            "function twoSum(a,t) { return [0,1]; }\n", "javascript", "blind75_two_sum"
        )
        fixture["prefix"] = "const Probe = { invert(x) { return x; } };\n"
        self.assertFalse(audit_envelope(fixture)["success"])
        fixture["prefix"] = (
            "class ListNode { constructor(value) { this.val=value; } }\n"
        )
        self.assertTrue(audit_envelope(fixture)["success"])

    def test_exact_transitive_helper_closure_is_allowed_but_extra_method_is_rejected(
        self,
    ):
        code = "function run(a,b) { return TreeAlgorithms.subtree(a,b); }\nconst TreeAlgorithms = { same(a,b) { return a===b; }, subtree(a,b) { return this.same(a,b); } };\n"
        errors, decisions = helper_dependencies(code, "javascript")
        self.assertEqual(errors, [])
        self.assertEqual(decisions[0]["reachableMethods"], ["same", "subtree"])
        extra = code.replace("same(a,b) {", "invert(a) { return a; }, same(a,b) {")
        self.assertTrue(helper_dependencies(extra, "javascript")[0])

    def test_python_helper_closure_is_checked(self):
        code = "def run(a, b):\n    return TreeAlgorithms.same(a, b)\n\nclass TreeAlgorithms:\n    @staticmethod\n    def same(a, b):\n        return a == b\n"
        self.assertEqual(helper_dependencies(code, "python")[0], [])
        extra = (
            code + "\n    @staticmethod\n    def invert(node):\n        return node\n"
        )
        self.assertTrue(helper_dependencies(extra, "python")[0])

    def test_callback_reference_requires_the_visible_helper_definition(self):
        code = "function run(lists) { return lists.flatMap(ListAlgorithms.nodes); }\nconst ListAlgorithms = { nodes(head) { return [head]; } };\n"
        self.assertEqual(helper_dependencies(code, "javascript")[0], [])
        missing = (
            "function run(lists) { return lists.flatMap(ListAlgorithms.nodes); }\n"
        )
        self.assertTrue(helper_dependencies(missing, "javascript")[0])
        wrong_member = code.replace("nodes(head)", "invert(head)")
        self.assertTrue(helper_dependencies(wrong_member, "javascript")[0])

    def test_transitive_callback_reference_is_reachable(self):
        code = "function run(lists) { return ListAlgorithms.flatten(lists); }\nconst ListAlgorithms = { flatten(lists) { return lists.flatMap(this.nodes); }, nodes(head) { return [head]; } };\n"
        errors, decisions = helper_dependencies(code, "javascript")
        self.assertEqual(errors, [])
        self.assertEqual(decisions[0]["reachableMethods"], ["flatten", "nodes"])

    def test_unrelated_free_algorithm_is_rejected(self):
        fixture = entry("", "javascript", "blind75_two_sum")
        code = "function twoSum(a,t) { return [0,1]; }\nfunction solveDifferentProblem(x) { return x; }\n"
        errors, _ = isolated_global_dependencies(fixture, code, "solution")
        self.assertTrue(any("solveDifferentProblem" in error for error in errors))
        needed = "function twoSum(a,t) { return findPair(a,t); }\nfunction findPair(a,t) { return [0,1]; }\n"
        self.assertEqual(
            isolated_global_dependencies(fixture, needed, "solution")[0], []
        )
        self.assertTrue(isolated_global_dependencies(fixture, needed, "starter")[0])

    def test_cpp_generic_task_class_is_a_visible_definition(self):
        fixture = entry("", "cpp")
        code = "template<class T> class Box { public: T value; };"
        with patch("audit.isolated_roots", return_value={"Box"}):
            self.assertEqual(
                isolated_global_dependencies(fixture, code, "starter")[0], []
            )
            self.assertTrue(
                isolated_global_dependencies(
                    fixture, code + " int unrelated(){return 0;}", "starter"
                )[0]
            )

    def test_python_generic_type_parameters_are_not_unrelated_algorithms(self):
        fixture = entry("", "python")
        code = 'from typing import Generic, TypeVar\nT = TypeVar("T")\nclass Box(Generic[T]):\n    pass\n'
        with patch("audit.isolated_roots", return_value={"Box"}):
            self.assertEqual(
                isolated_global_dependencies(fixture, code, "starter")[0], []
            )
            self.assertTrue(
                isolated_global_dependencies(
                    fixture, code + '\nUnused = TypeVar("Unused")\n', "starter"
                )[0]
            )
            helper = (
                code.replace("pass", "def run(self):\n        return helper()")
                + "\ndef helper():\n    return 0\n"
            )
            self.assertTrue(isolated_global_dependencies(fixture, helper, "starter")[0])

    def test_cpp_function_pointer_helper_reference_is_checked(self):
        code = "int Run(int x) { return Apply(TreeAlgorithms::same, x); }\nnamespace TreeAlgorithms { int same(int x) { return x; } }\n"
        self.assertEqual(helper_dependencies(code, "cpp")[0], [])
        self.assertTrue(helper_dependencies(code.split("namespace")[0], "cpp")[0])

    def test_java_method_reference_is_checked(self):
        code = "class Solution { Object run(Object values) { return apply(TreeAlgorithms::same,values); } }\nclass TreeAlgorithms { static int same(int x) { return x; } }\n"
        self.assertEqual(helper_dependencies(code, "java")[0], [])
        self.assertTrue(
            helper_dependencies(code.split("\nclass TreeAlgorithms")[0], "java")[0]
        )

    def test_compacted_method_is_rejected_even_when_syntax_is_valid(self):
        code = "public class Solution { public int Run(int n) { return n; } }\n"
        result = audit_artifact(entry(code), "solution")
        self.assertFalse(result["success"])
        self.assertIn(
            "Visible code is not in the pinned readable format", result["errors"]
        )

    def test_apple_stocks_references_must_be_empty(self):
        fixture = entry(
            format_code(
                "public class Solution { public int GetMaxProfit(int[] p) { return 0; } }",
                "csharp",
            )
        )
        fixture["references"] = [
            {
                "title": "Provided LinkedListNode",
                "names": ["LinkedListNode"],
                "code": format_code(
                    "public class LinkedListNode { public int Value; }", "csharp"
                ),
            }
        ]
        rows = audit_references(fixture)
        self.assertTrue(
            any(
                not row["success"] and "Expected only []" in " ".join(row["errors"])
                for row in rows
            )
        )

    def test_tree_reference_is_required_but_not_editable(self):
        fixture = entry(
            format_code(
                "public class Solution { public bool IsBalanced(BinaryTreeNode root) { return true; } }",
                "csharp",
            ),
            problem_id="interviewcake_balanced-binary-tree",
        )
        self.assertFalse(all(row["success"] for row in audit_references(fixture)))
        fixture["references"] = [
            {
                "title": "Provided BinaryTreeNode",
                "names": ["BinaryTreeNode"],
                "code": format_code(
                    "public class BinaryTreeNode { public int Value; public BinaryTreeNode Left, Right; }",
                    "csharp",
                ),
            }
        ]
        self.assertTrue(all(row["success"] for row in audit_references(fixture)))

    def test_random_injection_is_not_a_user_api_reference(self):
        fixture = entry("class Solution {}\n", "javascript", "interviewcake_shuffle")
        fixture["references"] = [
            {
                "title": "RandomSource",
                "names": ["RandomSource"],
                "code": format_code(
                    "class RandomSource { static Draw(a,b) {return a;} static GetRandom(a,b) {return a;} }",
                    "javascript",
                ),
            }
        ]
        self.assertTrue(
            any(
                "injection" in " ".join(row["errors"])
                for row in audit_references(fixture)
            )
        )

    def test_known_csharp_parser_bug_does_not_allow_another_syntax_error(self):
        original = "public class Solution { public int Run(string[] words) { var required = new Dictionary<string, int>(); foreach (string word in words) required[word] = required.GetValueOrDefault(word) + 1; return 0; } }"
        fixture = entry(
            format_code(original, "csharp"),
            problem_id="string_decompositions_into_dictionary_words",
        )
        result = audit_artifact(fixture, "solution", original=original)
        self.assertTrue(result["success"])
        self.assertEqual(len(result["syntaxExceptions"]), 1)
        broken = copy.deepcopy(fixture)
        broken["solutionCode"] += "public int )\n"
        self.assertFalse(
            audit_artifact(broken, "solution", check_format=False, original=original)[
                "success"
            ]
        )


if __name__ == "__main__":
    unittest.main()
