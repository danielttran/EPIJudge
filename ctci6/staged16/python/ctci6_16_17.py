def MaximumContiguousSum(values: list[int]) -> int:
    running = 0
    best = 0
    for value in values:
        running = max(0, running + value)
        best = max(best, running)
    return best
