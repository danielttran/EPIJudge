"""Order-insensitive completeness, duplicate rejection and input-identity checks."""

import json
import unittest
from core import ROOT
from corpus08 import canonical, oracle, valid_observation
from runtime import generate_runtime
from verify01 import execute


class CombinatorialContractTests(unittest.TestCase):
    def test_power_set_accepts_reordered_members_and_subsets(self):
        case = dict(arguments=[[3, 1]], expected=[[], [3], [1], [3, 1]])
        self.assertTrue(
            valid_observation(
                "8.4", case, dict(actual=[[1, 3], [1], [], [3]], mutationOk=True)
            )
        )
        for actual in (
            [[], [3], [1]],
            [[], [3], [1], [3, 1], [1, 3]],
            [[], [3], [1], [3, 3]],
            [[], [3], [True], [3, 1]],
        ):
            self.assertFalse(
                valid_observation("8.4", case, dict(actual=actual, mutationOk=True))
            )
        self.assertFalse(
            valid_observation(
                "8.4", case, dict(actual=case["expected"], mutationOk=False)
            )
        )

    def test_empty_and_maximum_set_outputs_are_complete(self):
        self.assertEqual([[]], oracle("8.4", [[]]))
        output = oracle("8.4", [list(range(12))])
        self.assertEqual(4096, len(output))
        self.assertEqual(4096, len(set(canonical("8.4", output))))

    def test_permutation_counts_and_duplicates(self):
        self.assertEqual([""], oracle("8.7", [""]))
        self.assertEqual(40320, len(oracle("8.7", ["abcdefgh"])))
        self.assertEqual(["aab", "aba", "baa"], oracle("8.8", ["aab"]))
        self.assertEqual(2520, len(oracle("8.8", ["aabbccdd"])))
        case = dict(expected=["aab", "aba", "baa"])
        self.assertTrue(
            valid_observation(
                "8.8", case, dict(actual=["baa", "aab", "aba"], mutationOk=True)
            )
        )
        self.assertFalse(
            valid_observation(
                "8.8", case, dict(actual=["aab", "aab", "baa"], mutationOk=True)
            )
        )

    def test_parenthesis_generation_counts_and_rejection(self):
        self.assertEqual(
            [1, 1, 2, 5, 14, 42, 132, 429, 1430],
            [len(oracle("8.9", [pairs])) for pairs in range(9)],
        )
        case = dict(expected=["(())", "()()"])
        for actual in (["(())", "(())"], ["(())", ")(()"], ["(())"], []):
            self.assertFalse(
                valid_observation("8.9", case, dict(actual=actual, mutationOk=True))
            )

    def test_collection_type_and_mutation_marker_are_explicit(self):
        for actual in (None, 0, {}, [True], ["a", 1]):
            self.assertFalse(
                valid_observation(
                    "8.7", dict(expected=["a"]), dict(actual=actual, mutationOk=True)
                )
            )
        self.assertFalse(
            valid_observation(
                "8.7", dict(expected=["a"]), dict(actual=["a"], mutationOk=1)
            )
        )


class CombinatorialRuntimeTests(unittest.TestCase):
    def test_python_input_integer_cannot_be_replaced_by_equal_boolean(self):
        generate_runtime()
        entry = next(
            e
            for e in json.loads((ROOT / "ctci6/runtime/catalog.json").read_text())
            if e["ref"] == "8.4"
        )
        config = entry["languages"]["python"]
        source = (
            config["prefix"]
            + config["solutionCode"]
            + """
_original = PowerSet
def PowerSet(values):
    result = _original(values)
    values[0] = True
    return result
"""
        )
        observed = execute(
            "python",
            False,
            [dict(ref="8.4", arguments=[[1]])],
            ROOT / ".epi-runs/ctci6-combinatorial-mutation",
            source_builder=lambda _language, _starter: config["harness"],
            companion_files={"solution.py": source},
        )[0]["observation"]
        self.assertEqual([[], [1]], observed["actual"])
        self.assertFalse(observed["mutationOk"])
        self.assertFalse(valid_observation("8.4", dict(expected=[[], [1]]), observed))


if __name__ == "__main__":
    unittest.main()
