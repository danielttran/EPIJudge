"""Stdlib regressions for the displayed sampler's equivalent statistical check."""

from __future__ import annotations

import importlib.util
import itertools
import random
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "epi_judge_python"))
from test_framework.random_sequence_checker import (
    check_birthday_spacings as original_birthday_check,
)
from test_framework.test_failure import TestFailure

specification = importlib.util.spec_from_file_location(
    "displayed_uniform_random", ROOT / "solutions/python/uniform_random_number.py"
)
assert specification is not None and specification.loader is not None
solution = importlib.util.module_from_spec(specification)
specification.loader.exec_module(solution)


class DirectExecutor:
    def __init__(self):
        self.calls = 0

    def run(self, function):
        self.calls += 1
        return function()


class RandomCheckerTests(unittest.TestCase):
    def test_exhaustive_window_counts_match_rebuilding_every_original_window(self):
        comparisons = 0
        for length in range(9):
            for sequence in itertools.product(range(3), repeat=length):
                for width in range(1, length + 1):
                    expected = sum(
                        len(set(sequence[start : start + width])) < width
                        for start in range(length - width)
                    )
                    self.assertEqual(
                        solution._count_repeated_windows(sequence, width), expected
                    )
                    comparisons += 1
        self.assertEqual(comparisons, 73812)

    def test_original_boolean_predicate_matches_at_size_and_domain_boundaries(self):
        rng = random.Random(738193)
        comparisons = 0
        for size in [0, 1, 999, 1000, 1001, 1200, 1500]:
            for domain in [1, 2, 3, 7, 100, 1000, 10000, 2**32]:
                sequences = [
                    [0] * size,
                    [index % domain for index in range(size)],
                    [rng.randrange(domain) for _ in range(size)],
                ]
                for sequence in sequences:
                    self.assertEqual(
                        solution._check_birthday_spacings(sequence, domain),
                        original_birthday_check(sequence, domain),
                    )
                    comparisons += 1
        self.assertEqual(comparisons, 168)

    def test_original_excluded_final_window_is_preserved(self):
        self.assertEqual(solution._count_repeated_windows([0, 1, 2, 2], 2), 0)
        self.assertEqual(solution._count_repeated_windows([0, 0, 1, 2], 2), 1)

    def test_rejection_sampler_consumes_fair_bits_and_supports_signed_endpoints(self):
        bits = iter([1, 1, 0, 1])
        with patch.object(solution, "zero_one_random", new=lambda: next(bits)):
            self.assertEqual(solution.uniform_random(7, 9), 8)
        with patch.object(solution, "zero_one_random", new=lambda: 1):
            self.assertEqual(solution.uniform_random(-(2**31), 2**31 - 1), 2**31 - 1)
        with patch.object(
            solution, "zero_one_random", side_effect=AssertionError("No bit is needed")
        ):
            self.assertEqual(solution.uniform_random(-(2**31), -(2**31)), -(2**31))

    def test_constant_and_cyclic_outputs_keep_all_samples_and_five_retries(self):
        for domain, cyclic in [(2, False), (4, True)]:
            calls = 0

            def incorrect(_lower, _upper, cycle=cyclic, outcomes=domain):
                nonlocal calls
                value = calls % outcomes if cycle else 0
                calls += 1
                return value

            executor = DirectExecutor()
            with (
                patch.object(solution, "uniform_random", new=incorrect),
                self.assertRaises(TestFailure),
            ):
                solution.uniform_random_wrapper(executor, 0, domain - 1)
            self.assertEqual(calls, 500000)
            self.assertEqual(executor.calls, 5)

    def test_singleton_out_of_range_output_is_rejected_with_original_sample_counts(
        self,
    ):
        calls = 0

        def incorrect(_lower, _upper):
            nonlocal calls
            calls += 1
            return 13

        # The legacy birthday/frequency checks accept a constant sequence for
        # one outcome; checking the actual interval is therefore essential.
        self.assertTrue(original_birthday_check([1] * 100000, 1))
        executor = DirectExecutor()
        with (
            patch.object(solution, "uniform_random", new=incorrect),
            self.assertRaises(TestFailure),
        ):
            solution.uniform_random_wrapper(executor, 12, 12)
        self.assertEqual(calls, 500000)
        self.assertEqual(executor.calls, 5)

    def test_frequency_pair_triple_thresholds_and_sample_volume_remain_unchanged(self):
        recorded = []
        samples = [9] * 100000

        def recording(name):
            def check(values, domain, tolerance):
                recorded.append((name, len(values), domain, tolerance))
                return True

            return check

        with (
            patch.object(solution, "check_frequencies", new=recording("marginal")),
            patch.object(solution, "check_pairs_frequencies", new=recording("pairs")),
            patch.object(
                solution, "check_triples_frequencies", new=recording("triples")
            ),
        ):
            self.assertTrue(solution._samples_are_uniform(samples, 9, 9))
        self.assertEqual(
            recorded,
            [
                ("marginal", 100000, 1, 0.01),
                ("pairs", 100000, 1, 0.01),
                ("triples", 100000, 1, 0.01),
            ],
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
