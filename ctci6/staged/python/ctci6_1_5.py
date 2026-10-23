def OneAway(first: str, second: str) -> bool:
    n, m = len(first), len(second)
    if abs(n - m) > 1:
        return False
    i = j = 0
    used = False
    while i < n and j < m:
        if first[i] == second[j]:
            i += 1
            j += 1
        else:
            if used:
                return False
            used = True
            if n >= m:
                i += 1
            if m >= n:
                j += 1
    return True
