def GenerateParentheses(pairs: int) -> list[str]:
    buffer = [""] * (2 * pairs)
    result = []

    def visit(opened, closed):
        position = opened + closed
        if position == len(buffer):
            result.append("".join(buffer))
            return
        if opened < pairs:
            buffer[position] = "("
            visit(opened + 1, closed)
        if closed < opened:
            buffer[position] = ")"
            visit(opened, closed + 1)

    visit(0, 0)
    return result
