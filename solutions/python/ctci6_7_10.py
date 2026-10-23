def PlayMinesweeper(bombs: list[list[int]], actions: list[list[int]]) -> list[list[int]]:
    rows, columns = len(bombs), len(bombs[0])
    visible = [[9] * columns for _ in bombs]
    safe = sum(value == 0 for row in bombs for value in row)
    state = 0
    trace = []

    def snapshot(accepted):
        trace.append([state, accepted] + [v for row in visible for v in row])

    def expose(row, column, queue):
        nonlocal safe
        if visible[row][column] != 9 or bombs[row][column]:
            return
        visible[row][column] = sum(
            bombs[r][c]
            for r in range(max(0, row - 1), min(rows, row + 2))
            for c in range(max(0, column - 1), min(columns, column + 2))
        )
        safe -= 1
        if visible[row][column] == 0:
            queue.append((row, column))

    snapshot(0)
    for row, column, kind in actions:
        accepted = 0
        if state == 0 and 0 <= row < rows and 0 <= column < columns:
            if kind == 1 and visible[row][column] in (9, 10):
                visible[row][column] = 19 - visible[row][column]
                accepted = 1
            elif kind == 0 and visible[row][column] == 9:
                accepted = 1
                if bombs[row][column]:
                    visible[row][column] = 11
                    state = 2
                else:
                    queue = []
                    expose(row, column, queue)
                    head = 0
                    while head < len(queue):
                        r, c = queue[head]
                        head += 1
                        for nr in range(max(0, r - 1), min(rows, r + 2)):
                            for nc in range(max(0, c - 1), min(columns, c + 2)):
                                expose(nr, nc, queue)
                    if safe == 0:
                        state = 1
        snapshot(accepted)
    return trace
