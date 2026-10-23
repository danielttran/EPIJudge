def PlayOthello(size: int, actions: list[list[int]]) -> list[list[int]]:
    board = [[0] * size for _ in range(size)]
    middle = size // 2
    board[middle - 1][middle - 1] = board[middle][middle] = 2
    board[middle - 1][middle] = board[middle][middle - 1] = 1
    trace = []

    def captures(row, column, color):
        if not (0 <= row < size and 0 <= column < size) or board[row][column] != 0:
            return []
        result = []
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == dc == 0:
                    continue
                r, c = row + dr, column + dc
                path = []
                while 0 <= r < size and 0 <= c < size and board[r][c] == 3 - color:
                    path.append((r, c))
                    r += dr
                    c += dc
                if path and 0 <= r < size and 0 <= c < size and board[r][c] == color:
                    result.extend(path)
        return result

    def can_move(color):
        return any(captures(r, c, color) for r in range(size) for c in range(size))

    def snapshot(accepted):
        flat = [v for row in board for v in row]
        trace.append([turn, accepted, flat.count(1), flat.count(2)] + flat)

    turn = 1 if can_move(1) else 0
    snapshot(0)
    for row, column, color in actions:
        accepted = 0
        if turn and color == turn:
            flipped = captures(row, column, color)
            if flipped:
                board[row][column] = color
                for r, c in flipped:
                    board[r][c] = color
                accepted = 1
                turn = 3 - color if can_move(3 - color) else color if can_move(color) else 0
        snapshot(accepted)
    return trace
