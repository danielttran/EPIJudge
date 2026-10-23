"""Execute regression fixtures that distinguish equality from object identity."""

import json
import unittest

from core import ROOT
from corpus02 import valid_observation
from models02 import MODELS
from runtime import generate_runtime
from verify01 import execute


class IdentityRuntimeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        generate_runtime()
        cls.entry = next(
            e
            for e in json.loads((ROOT / "ctci6/runtime/catalog.json").read_text())
            if e["ref"] == "2.2"
        )

    def run_fixture(self, language, source, case):
        configuration = self.entry["languages"][language]
        filename = "Solution.cs" if language == "csharp" else "solution.py"
        values = execute(
            language,
            False,
            [dict(ref="2.2", arguments=case["arguments"])],
            ROOT / ".epi-runs/ctci6-identity" / language,
            source_builder=lambda _language, _starters: configuration["harness"],
            companion_files={filename: source},
        )
        return values[0]["observation"]

    def test_python_equal_proxy_is_not_the_original_node(self):
        configuration = self.entry["languages"]["python"]
        source = (
            configuration["prefix"]
            + configuration["solutionCode"]
            + """
_original_kth = KthToLast
class EqualProxy(LinkedListNode):
    def __init__(self, original):
        super().__init__(original.Value, original.Next)
        self.original = original
    def __hash__(self):
        return hash(self.original)
    def __eq__(self, other):
        return other is self.original
def KthToLast(head, k):
    original = _original_kth(head, k)
    return None if original is None else EqualProxy(original)
"""
        )
        case = dict(arguments=[[7, 7], 1], expected=1)
        observed = self.run_fixture("python", source, case)
        self.assertEqual(observed["returnedId"], 2)
        self.assertFalse(valid_observation("2.2", case, observed))

    def test_csharp_value_equality_does_not_merge_original_nodes(self):
        configuration = self.entry["languages"]["csharp"]
        model = """public class LinkedListNode {
public int Value; public LinkedListNode? Next;
public LinkedListNode(int value,LinkedListNode? next=null){Value=value;Next=next;}
public override bool Equals(object? other)=>other is LinkedListNode n&&Value==n.Value;
public override int GetHashCode()=>Value;
}
"""
        self.assertEqual(configuration["prefix"].count(MODELS["csharp"]), 1)
        source = (
            configuration["prefix"].replace(MODELS["csharp"], model)
            + configuration["solutionCode"]
        )
        case = dict(arguments=[[7, 7], 2], expected=0)
        observed = self.run_fixture("csharp", source, case)
        self.assertEqual(observed["returnedId"], 0)
        self.assertTrue(valid_observation("2.2", case, observed))


if __name__ == "__main__":
    unittest.main()
