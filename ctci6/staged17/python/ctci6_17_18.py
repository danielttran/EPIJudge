def ShortestCoveringRange(big: list[int], small: list[int]) -> list[int]:
    if not small:
        return [-1, -1]
    counts = {value: 0 for value in small}
    missing = len(small)
    left = 0
    best_start = best_end = -1
    for right, value in enumerate(big):
        if value in counts:
            if counts[value] == 0:
                missing -= 1
            counts[value] += 1
        while missing == 0:
            if best_start == -1 or right - left < best_end - best_start:
                best_start, best_end = left, right
            removed = big[left]
            if removed in counts:
                counts[removed] -= 1
                if counts[removed] == 0:
                    missing += 1
            left += 1
    return [best_start, best_end]
