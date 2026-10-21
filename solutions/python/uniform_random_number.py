"""Original fair-bit sampler and equivalent linear-time statistical wrapper."""

import math
import random

from test_framework import generic_test
from test_framework.random_sequence_checker import (
    check_frequencies,
    check_pairs_frequencies,
    check_triples_frequencies,
    run_func_with_retries,
)
from test_framework.test_utils import enable_executor_hook


def zero_one_random():
    return random.randrange(2)


def uniform_random(lower_bound: int, upper_bound: int) -> int:
    outcomes = upper_bound - lower_bound + 1
    if outcomes <= 0:
        raise ValueError("The lower bound must not exceed the upper bound.")
    bit_count = (outcomes - 1).bit_length()
    while True:
        offset = 0
        for _ in range(bit_count):
            offset = 2 * offset + zero_one_random()
        if offset < outcomes:
            return lower_bound + offset


def _count_repeated_windows(sequence, width):
    """Count duplicate-containing windows at the native checker's endpoints."""
    frequencies = {}
    repeated_occurrences = 0
    for value in sequence[:width]:
        old_count = frequencies.get(value, 0)
        repeated_occurrences += old_count > 0
        frequencies[value] = old_count + 1

    repeated_windows = 0
    # Compatibility: the original checker excludes the final possible start.
    for start in range(len(sequence) - width):
        repeated_windows += repeated_occurrences > 0
        outgoing = sequence[start]
        old_count = frequencies[outgoing]
        repeated_occurrences -= old_count > 1
        if old_count == 1:
            del frequencies[outgoing]
        else:
            frequencies[outgoing] = old_count - 1
        incoming = sequence[start + width]
        old_count = frequencies.get(incoming, 0)
        repeated_occurrences += old_count > 0
        frequencies[incoming] = old_count + 1
    return repeated_windows


def _check_birthday_spacings(sequence, outcomes):
    width = math.ceil(math.sqrt(math.log(2) * 2.0 * outcomes))
    window_count = len(sequence) - width + 1
    if window_count < 1000:
        return True
    # Keep the original denominator, threshold and minimum sample-window rule.
    return 0.4 * window_count <= _count_repeated_windows(sequence, width)


def _samples_are_uniform(samples, lower_bound, upper_bound):
    outcomes = upper_bound - lower_bound + 1
    offsets = []
    for value in samples:
        if type(value) is not int:
            return False
        offset = value - lower_bound
        if not 0 <= offset < outcomes:
            return False
        offsets.append(offset)
    return (
        check_frequencies(offsets, outcomes, 0.01)
        and check_pairs_frequencies(offsets, outcomes, 0.01)
        and check_triples_frequencies(offsets, outcomes, 0.01)
        and _check_birthday_spacings(offsets, outcomes)
    )


@enable_executor_hook
def uniform_random_wrapper(executor, lower_bound, upper_bound):
    def check_once():
        samples = executor.run(
            lambda: [uniform_random(lower_bound, upper_bound) for _ in range(100000)]
        )
        return _samples_are_uniform(samples, lower_bound, upper_bound)

    # The unchanged framework helper allows exactly the original five attempts.
    run_func_with_retries(check_once)


if __name__ == "__main__":
    raise SystemExit(
        generic_test.generic_test_main(
            "uniform_random_number.py",
            "uniform_random_number.tsv",
            uniform_random_wrapper,
        )
    )
