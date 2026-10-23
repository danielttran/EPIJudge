def PermutationsWithDuplicates(text: str) -> list[str]:
    counts = [0] * 26
    for char in text:
        counts[ord(char) - ord("a")] += 1
    buffer = [""] * len(text)
    result = []

    def visit(depth):
        if depth == len(buffer):
            result.append("".join(buffer))
            return
        for letter in range(26):
            if counts[letter]:
                counts[letter] -= 1
                buffer[depth] = chr(ord("a") + letter)
                visit(depth + 1)
                counts[letter] += 1

    visit(0)
    return result
