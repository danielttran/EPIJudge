def MergeSortedIntoFirst(first: list[int], realCount: int, second: list[int]) -> list[int]:
    a, b, write = realCount - 1, len(second) - 1, len(first) - 1
    while b >= 0:
        if a >= 0 and first[a] > second[b]:
            first[write] = first[a]
            a -= 1
        else:
            first[write] = second[b]
            b -= 1
        write -= 1
    return first
