def PaintFill(screen: list[list[int]], row: int, column: int, newColor: int) -> list[list[int]]:
    rows = len(screen)
    columns = len(screen[0]) if rows else 0
    if row < 0 or row >= rows or column < 0 or column >= columns:
        return screen
    old_color = screen[row][column]
    if old_color == newColor:
        return screen
    work = [(row, column)]
    screen[row][column] = newColor
    while work:
        r, c = work.pop()
        for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
            if 0 <= nr < rows and 0 <= nc < columns and screen[nr][nc] == old_color:
                screen[nr][nc] = newColor
                work.append((nr, nc))
    return screen
