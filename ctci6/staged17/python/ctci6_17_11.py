def WordDistance(words: list[str], first: str, second: str) -> int:
    last_first = last_second = -1
    best = len(words) + 1
    for index, word in enumerate(words):
        if word == first:
            last_first = index
            if last_second >= 0:
                best = min(best, index - last_second)
        elif word == second:
            last_second = index
            if last_first >= 0:
                best = min(best, index - last_first)
    return -1 if best == len(words) + 1 else best
