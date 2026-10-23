def LargestBlackBorder(matrix: list[list[int]]) -> list[int]:
    n = len(matrix)
    right = [[0] * n for _ in range(n)]
    down = [[0] * n for _ in range(n)]
    for row in range(n - 1, -1, -1):
        for column in range(n - 1, -1, -1):
            if matrix[row][column] == 0:
                right[row][column] = 1 + (right[row][column + 1] if column + 1 < n else 0)
                down[row][column] = 1 + (down[row + 1][column] if row + 1 < n else 0)
    for size in range(n, 0, -1):
        for row in range(n - size + 1):
            for column in range(n - size + 1):
                if (
                    right[row][column] >= size
                    and down[row][column] >= size
                    and right[row + size - 1][column] >= size
                    and down[row][column + size - 1] >= size
                ):
                    return [row, column, size]
    return []
