def TicTacWinner(board: list[list[int]]) -> int:
    n = len(board)
    if n == 0:
        return 0
    for index in range(n):
        row_player = board[index][0]
        column_player = board[0][index]
        if row_player and all(board[index][j] == row_player for j in range(n)):
            return row_player
        if column_player and all(board[j][index] == column_player for j in range(n)):
            return column_player
    main = board[0][0]
    other = board[0][n - 1]
    if main and all(board[i][i] == main for i in range(n)):
        return main
    if other and all(board[i][n - 1 - i] == other for i in range(n)):
        return other
    return 0
