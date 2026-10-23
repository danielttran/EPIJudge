def CountTripleSteps(steps: int) -> int:
    if steps < 0:
        return 0
    previous, older, oldest = 1, 0, 0
    for _ in range(steps):
        current = previous + older + oldest
        oldest, older, previous = older, previous, current
    return previous
