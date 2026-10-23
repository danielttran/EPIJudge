def LangtonBoard(steps: int) -> list[str]:
    black = set()
    row = column = direction = 0
    min_row = max_row = min_column = max_column = 0
    dr, dc = [0, 1, 0, -1], [1, 0, -1, 0]
    for _ in range(steps):
        position = (row, column)
        if position in black:
            direction = (direction + 3) % 4
            black.remove(position)
        else:
            direction = (direction + 1) % 4
            black.add(position)
        row += dr[direction]
        column += dc[direction]
        min_row, max_row = min(min_row, row), max(max_row, row)
        min_column, max_column = min(min_column, column), max(max_column, column)
    result = []
    for r in range(min_row, max_row + 1):
        line = []
        for c in range(min_column, max_column + 1):
            line.append(
                "RDLU"[direction] if (r, c) == (row, column) else "#" if (r, c) in black else "."
            )
        result.append("".join(line))
    return result
