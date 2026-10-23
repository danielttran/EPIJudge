def EightQueens() -> list[list[int]]:
    board = [0] * 8
    result = []

    def visit(row, used_columns, used_down, used_up):
        if row == 8:
            result.append(board.copy())
            return
        for column in range(8):
            col_bit = 1 << column
            down_bit = 1 << (row - column + 7)
            up_bit = 1 << (row + column)
            if used_columns & col_bit or used_down & down_bit or used_up & up_bit:
                continue
            board[row] = column
            visit(row + 1, used_columns | col_bit, used_down | down_bit, used_up | up_bit)

    visit(0, 0, 0, 0)
    return result
