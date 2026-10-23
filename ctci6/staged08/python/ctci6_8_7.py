def PermutationsDistinct(text: str) -> list[str]:
    chars = list(text)
    result = []

    def visit(depth):
        if depth == len(chars):
            result.append("".join(chars))
            return
        for index in range(depth, len(chars)):
            chars[depth], chars[index] = chars[index], chars[depth]
            visit(depth + 1)
            chars[depth], chars[index] = chars[index], chars[depth]

    visit(0)
    return result
