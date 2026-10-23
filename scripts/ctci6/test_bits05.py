"""Independent bit-contract properties and strict primitive result grading."""

import random
import unittest

from corpus05 import oracle, signed, valid_observation


class BitContractTests(unittest.TestCase):
    def test_full_width_insertion_preserves_signed_pattern(self):
        for word in (-2147483648, -1, 0, 2147483647):
            for replacement in (-2147483648, -1, 0, 2147483647):
                self.assertEqual(replacement, oracle("5.1", [word, replacement, 0, 31]))

    def test_insertion_clears_only_selected_bits(self):
        for low in range(32):
            for high in range(low, 32):
                actual = oracle("5.1", [-1, 0, low, high]) & 0xFFFFFFFF
                for bit in range(32):
                    self.assertEqual(not low <= bit <= high, bool((actual >> bit) & 1))

    def test_conversion_is_exact_for_sign_bit_and_all_bits(self):
        self.assertEqual(32, oracle("5.6", [0, -1]))
        self.assertEqual(1, oracle("5.6", [-2147483648, 0]))
        self.assertEqual(0, oracle("5.6", [-1, -1]))

    def test_adjacent_swap_is_involution_and_preserves_population(self):
        rng = random.Random(657)
        values = [-2147483648, -1, 0, 2147483647] + [
            rng.randrange(-(2**31), 2**31) for _ in range(200)
        ]
        for word in values:
            swapped = oracle("5.7", [word])
            self.assertEqual(word, oracle("5.7", [swapped]))
            self.assertEqual(oracle("5.6", [word, 0]), oracle("5.6", [swapped, 0]))
        for bit in range(32):
            self.assertEqual(signed(1 << (bit ^ 1)), oracle("5.7", [signed(1 << bit)]))

    def test_grading_does_not_accept_bool_or_unsigned_alias(self):
        self.assertFalse(
            valid_observation(dict(expected=1), dict(actual=True, mutationOk=True))
        )
        self.assertFalse(
            valid_observation(
                dict(expected=-1), dict(actual=4294967295, mutationOk=True)
            )
        )
        self.assertFalse(
            valid_observation(dict(expected=0), dict(actual=0, mutationOk=1))
        )
        self.assertFalse(valid_observation(dict(expected=0), None))


if __name__ == "__main__":
    unittest.main()
