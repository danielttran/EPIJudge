def ContinuousMedians(values: list[int]) -> list[float]:
    from heapq import heappush, heappop

    lower = []
    upper = []
    medians = []
    for value in values:
        if not lower or value <= -lower[0]:
            heappush(lower, -value)
        else:
            heappush(upper, value)
        if len(lower) > len(upper) + 1:
            heappush(upper, -heappop(lower))
        elif len(upper) > len(lower):
            heappush(lower, -heappop(upper))
        medians.append(
            float(-lower[0]) if len(lower) > len(upper) else (-lower[0] + upper[0]) / 2.0
        )
    return medians
