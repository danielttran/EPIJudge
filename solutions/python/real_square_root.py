import math

from test_framework import generic_test


def square_root(x: float) -> float:
    if x == 0:
        return 0.0
    low, high = 0.0, max(1.0, x)
    for _ in range(1100):
        middle = low + (high - low) / 2
        if middle == low or middle == high:
            break
        if middle <= x / middle:
            low = middle
        else:
            high = middle
    return low + (high - low) / 2
