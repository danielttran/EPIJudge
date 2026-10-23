def MaximumWithoutComparison(first: int, second: int) -> int:
    negative_first = (first >> 31) & 1
    negative_second = (second >> 31) & 1
    negative_difference = ((first - second) & 0xFFFFFFFF) >> 31
    different = negative_first ^ negative_second
    choose_first = different * (negative_first ^ 1) + (different ^ 1) * (negative_difference ^ 1)
    mask = -choose_first
    return (first & mask) | (second & ~mask)
