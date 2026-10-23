def MaximumSubmatrix(matrix: list[list[int]]) -> list[int]:
    rows = len(matrix)
    columns = len(matrix[0]) if rows else 0
    if not rows or not columns:
        return []
    best = -2147483648
    answer = []
    for top in range(rows):
        totals = [0] * columns
        for bottom in range(top, rows):
            running = start = 0
            for column in range(columns):
                totals[column] += matrix[bottom][column]
                if running < 0:
                    running = totals[column]
                    start = column
                else:
                    running += totals[column]
                if running > best:
                    best = running
                    answer = [best, top, start, bottom, column]
    return answer
