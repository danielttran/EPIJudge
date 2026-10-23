def CheckPermutation(first: str, second: str) -> bool:
    if len(first) != len(second):
        return False
    counts = [0] * 128
    for character in first:
        counts[ord(character)] += 1
    for character in second:
        code = ord(character)
        counts[code] -= 1
        if counts[code] < 0:
            return False
    return True
