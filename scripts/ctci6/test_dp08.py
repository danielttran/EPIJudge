"""Count conventions and independent reference sanity checks for the first DP batch."""

import unittest
from corpus08 import oracle, valid_observation


class DpContractTests(unittest.TestCase):
    def test_ordered_hops_and_empty_route(self):
        self.assertEqual(
            [1, 1, 2, 4, 7, 13, 24, 44, 81, 149, 274],
            [oracle("8.1", [n]) for n in range(11)],
        )
        self.assertEqual(0, oracle("8.1", [-2147483648]))
        self.assertEqual(2082876103, oracle("8.1", [36]))

    def test_recursive_product_domain_boundaries(self):
        for first, second, expected in (
            (0, 46340, 0),
            (1, 46340, 46340),
            (46340, 46340, 2147395600),
            (7, 12, 84),
            (12, 7, 84),
        ):
            self.assertEqual(expected, oracle("8.5", [first, second]))

    def test_combinations_are_not_sequences_or_minimum_coins(self):
        for amount, expected in (
            (0, 1),
            (1, 1),
            (4, 1),
            (5, 2),
            (10, 4),
            (25, 13),
            (100, 242),
        ):
            self.assertEqual(expected, oracle("8.11", [amount]))
        self.assertLessEqual(oracle("8.11", [10000]), 2147483647)

    def test_primitive_grading_rejects_boolean_and_incomplete_observation(self):
        for observed in (
            dict(actual=True, mutationOk=True),
            dict(actual=1, mutationOk=1),
            dict(actual=1),
            None,
        ):
            self.assertFalse(valid_observation("8.1", dict(expected=1), observed))


if __name__ == "__main__":
    unittest.main()
