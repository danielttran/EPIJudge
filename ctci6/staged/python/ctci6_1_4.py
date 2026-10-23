def PalindromePermutation(text: str) -> bool:
    counts = [0] * 128
    for character in text:
        code = ord(character)
        if 65 <= code <= 90:
            code += 32
        if 97 <= code <= 122:
            counts[code] += 1
    return sum(counts[code] % 2 for code in range(97, 123)) <= 1
