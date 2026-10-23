def SmallestDifference(first: list[int], second: list[int]) -> int:
    if not first or not second:
        return -1
    a, b = sorted(first), sorted(second)
    i = j = 0
    best = 4294967295
    while i < len(a) and j < len(b):
        difference = a[i] - b[j]
        best = min(best, abs(difference))
        if difference == 0:
            return 0
        if difference < 0:
            i += 1
        else:
            j += 1
    return best
