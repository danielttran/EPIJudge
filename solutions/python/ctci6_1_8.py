def ZeroMatrix(matrix: list[list[int]]) -> None:
    rows = len(matrix)
    if rows == 0:
        return
    cols = len(matrix[0])
    zero_rows, zero_cols = [False] * rows, [False] * cols
    for r in range(rows):
        for c in range(cols):
            if matrix[r][c] == 0:
                zero_rows[r] = True
                zero_cols[c] = True
    for r in range(rows):
        for c in range(cols):
            if zero_rows[r] or zero_cols[c]:
                matrix[r][c] = 0
