"""State-contract and actual submitted-object identity regressions."""

import copy
import json
import unittest

from core import EXT, LANGUAGES, ROOT
from corpus03 import oracle, valid_observation
from runtime import generate_runtime
from verify01 import execute


class StateGraderTests(unittest.TestCase):
    def assert_result(self, ref, arguments, expected):
        self.assertEqual(expected, oracle(ref, arguments))
        case = dict(arguments=arguments, expected=expected)
        self.assertTrue(valid_observation(case, dict(actual=expected, mutationOk=True)))
        self.assertFalse(
            valid_observation(case, dict(actual=expected, mutationOk=False))
        )

    def test_three_stacks_error_priority_and_unchanged_payload(self):
        self.assert_result(
            "3.1",
            [
                [
                    "ThreeStacks",
                    "Push",
                    "Push",
                    "Push",
                    "Peek",
                    "Pop",
                    "Pop",
                    "IsEmpty",
                ],
                [[1], [0, 7], [0, 8], [3, 9], [0], [0], [0], [1]],
            ],
            [
                None,
                None,
                {"error": "full"},
                {"error": "index"},
                7,
                7,
                {"error": "empty"},
                True,
            ],
        )

    def test_repeated_minimum_and_integer_endpoints(self):
        self.assert_result(
            "3.2",
            [
                ["MinStack", "Push", "Push", "Push", "Pop", "GetMin", "Pop", "GetMin"],
                [[], [2147483647], [-2147483648], [-2147483648], [], [], [], []],
            ],
            [None, None, None, None, -2147483648, -2147483648, -2147483648, 2147483647],
        )

    def test_rollover_compacts_later_indices(self):
        self.assert_result(
            "3.3",
            [
                ["SetOfStacks"]
                + ["Push"] * 5
                + ["PopAt", "PopAt", "Pop", "PopAt", "Pop"],
                [[2]] + [[i] for i in range(1, 6)] + [[0], [1], [], [1], []],
            ],
            [None] * 6 + [2, 5, 4, {"error": "index"}, 3],
        )

    def test_queue_does_not_transfer_ahead_of_older_output(self):
        self.assert_result(
            "3.4",
            [
                [
                    "TwoStackQueue",
                    "Add",
                    "Add",
                    "Remove",
                    "Add",
                    "Peek",
                    "Remove",
                    "Remove",
                    "Remove",
                    "Size",
                ],
                [[], [6], [2], [], [9], [], [], [], [], []],
            ],
            [None, None, None, 6, None, 2, 2, 9, {"error": "empty"}, 0],
        )

    def test_sort_observation_keeps_duplicate_multiplicity(self):
        case = dict(arguments=[[2, 1, 2]], expected=[1, 2, 2])
        self.assertTrue(
            valid_observation(case, dict(actual=[1, 2, 2], mutationOk=True))
        )
        self.assertFalse(valid_observation(case, dict(actual=[1, 2], mutationOk=True)))
        self.assertFalse(
            valid_observation(case, dict(actual=[2, 2, 1], mutationOk=True))
        )

    def test_invalid_species_is_not_admitted_and_age_is_not_id(self):
        self.assert_result(
            "3.6",
            [
                [
                    "AnimalShelter",
                    "Enqueue",
                    "Enqueue",
                    "Enqueue",
                    "DequeueAny",
                    "DequeueDog",
                    "Size",
                    "DequeueCat",
                ],
                [[], [50, "dog"], [-100, "fish"], [2, "cat"], [], [], [], []],
            ],
            [None, None, {"error": "species"}, None, 50, None, 1, 2],
        )

    def test_wire_values_require_boolean_integer_and_null_types(self):
        for expected, wrong in [
            (True, 1),
            (1, True),
            (None, 0),
            ({"error": "empty"}, {"error": "empty", "extra": True}),
        ]:
            with self.subTest(expected=expected):
                self.assertFalse(
                    valid_observation(
                        dict(expected=[expected]), dict(actual=[wrong], mutationOk=True)
                    )
                )
        self.assertFalse(valid_observation(dict(expected=[]), None))
        self.assertFalse(
            valid_observation(dict(expected=[]), dict(actual=[], mutationOk=1))
        )


class AnimalIdentityRuntimeTests(unittest.TestCase):
    def test_equal_valued_copies_are_rejected_in_every_language(self):
        generate_runtime()
        entry = next(
            e
            for e in json.loads((ROOT / "ctci6/runtime/catalog.json").read_text())
            if e["ref"] == "3.6"
        )
        edits = {
            "csharp": (
                "return entry.Value;",
                "return new Animal(entry.Value.Id, entry.Value.Species);",
            ),
            "javascript": (
                "return entry.value;",
                "return new Animal(entry.value.Id, entry.value.Species);",
            ),
            "python": (
                "return entry.value",
                "return Animal(entry.value.Id, entry.value.Species)",
            ),
            "cpp": ("return value;", "return new Animal(value->Id, value->Species);"),
            "java": (
                "return entry.Value;",
                "return new Animal(entry.Value.Id, entry.Value.Species);",
            ),
        }
        case = dict(
            arguments=[
                ["AnimalShelter", "Enqueue", "DequeueAny"],
                [[], [50, "dog"], []],
            ],
            expected=[None, None, 50],
        )
        for language in LANGUAGES:
            with self.subTest(language=language):
                config = entry["languages"][language]
                before, after = edits[language]
                self.assertEqual(config["solutionCode"].count(before), 1)
                source = (
                    config["prefix"]
                    + config["solutionCode"].replace(before, after)
                    + config["suffix"]
                )
                filename = (
                    "Solution." if language in ("csharp", "java") else "solution."
                ) + EXT[language]
                observed = execute(
                    language,
                    False,
                    [dict(ref="3.6", arguments=copy.deepcopy(case["arguments"]))],
                    ROOT / ".epi-runs/ctci6-animal-clones" / language,
                    source_builder=lambda _language, _starter: config["harness"],
                    companion_files={filename: source},
                )[0]["observation"]
                self.assertFalse(observed["mutationOk"])
                self.assertFalse(valid_observation(case, observed))


if __name__ == "__main__":
    unittest.main()
