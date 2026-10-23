def LongestLettersDigits(text: str) -> list[int]:
    n = len(text)
    first = [-2] * (2 * n + 1)
    first[n] = -1
    balance = best = 0
    start = end = -1
    for index, char in enumerate(text):
        balance += -1 if "0" <= char <= "9" else 1
        slot = balance + n
        if first[slot] == -2:
            first[slot] = index
        elif index - first[slot] > best:
            best = index - first[slot]
            start, end = first[slot] + 1, index
    return [start, end]
