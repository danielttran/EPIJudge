def MatchesPattern(pattern: str, text: str) -> bool:
    if not pattern:
        return not text
    count_a = pattern.count("a")
    count_b = len(pattern) - count_a
    maximum = len(text) // count_a if count_a else 0
    for length_a in range(maximum + 1):
        remaining = len(text) - count_a * length_a
        if count_b == 0:
            if remaining != 0:
                continue
            length_b = 0
        else:
            if remaining % count_b:
                continue
            length_b = remaining // count_b
        a = b = None
        offset = 0
        valid = True
        for symbol in pattern:
            length = length_a if symbol == "a" else length_b
            part = text[offset : offset + length]
            if symbol == "a":
                if a is None:
                    a = part
                elif a != part:
                    valid = False
                    break
            else:
                if b is None:
                    b = part
                elif b != part:
                    valid = False
                    break
            offset += length
        if valid and offset == len(text):
            return True
    return False
