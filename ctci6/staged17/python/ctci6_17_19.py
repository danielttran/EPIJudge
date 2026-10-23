def MissingTwo(values: list[int]) -> list[int]:
    n = len(values) + 2
    combined = 0
    for value in range(1, n + 1):
        combined ^= value
    for value in values:
        combined ^= value
    bit = combined & -combined
    first = second = 0
    for value in range(1, n + 1):
        if value & bit:
            first ^= value
        else:
            second ^= value
    for value in values:
        if value & bit:
            first ^= value
        else:
            second ^= value
    return [min(first, second), max(first, second)]
