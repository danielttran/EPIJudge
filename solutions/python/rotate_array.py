from typing import List

from test_framework import generic_test
from test_framework.test_utils import enable_executor_hook


def rotate_array(rotate_amount: int, A: List[int]) -> None:
    if not A:
        return
    shift = rotate_amount % len(A)

    def reverse_segment(first, last):
        while first < last:
            A[first], A[last] = A[last], A[first]
            first += 1
            last -= 1

    reverse_segment(0, len(A) - 1)
    reverse_segment(0, shift - 1)
    reverse_segment(shift, len(A) - 1)


@enable_executor_hook
def rotate_array_wrapper(executor, A, rotate_amount):
    rotated = list(A)
    executor.run(lambda: rotate_array(rotate_amount, rotated))
    return rotated


if __name__ == '__main__':
    raise SystemExit(generic_test.generic_test_main(
        'rotate_array.py', 'rotate_array.tsv', rotate_array_wrapper))
