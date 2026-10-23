def IsUnique(text: str) -> bool:
    seen = [False] * 128
    for character in text:
        code = ord(character)
        if seen[code]:
            return False
        seen[code] = True
    return True
