def Rotate(matrix: list[list[int]]) -> None:
    n = len(matrix)
    for r in range(n):
        for c in range(r + 1, n):
            matrix[r][c], matrix[c][r] = matrix[c][r], matrix[r][c]
    for r in range(n):
        for c in range(n // 2):
            matrix[r][c], matrix[r][n - 1 - c] = matrix[r][n - 1 - c], matrix[r][c]
