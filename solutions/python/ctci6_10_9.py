def SearchSortedMatrix(matrix: list[list[int]], target: int) -> list[int]:
    rows = len(matrix)
    columns = len(matrix[0]) if rows else 0
    row, column = 0, columns - 1
    while row < rows and column >= 0:
        value = matrix[row][column]
        if value == target:
            return [row, column]
        if value > target:
            column -= 1
        else:
            row += 1
    return [-1, -1]
