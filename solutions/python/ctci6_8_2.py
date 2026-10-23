def FindRobotPath(grid: list[list[int]]) -> list[list[int]]:
    rows = len(grid)
    columns = len(grid[0]) if rows else 0
    if not rows or not columns:
        return []
    parent = [[0] * columns for _ in range(rows)]
    for r in range(rows):
        for c in range(columns):
            if grid[r][c] == 0:
                continue
            if r == 0 and c == 0:
                parent[r][c] = 3
            elif r > 0 and parent[r - 1][c]:
                parent[r][c] = 1
            elif c > 0 and parent[r][c - 1]:
                parent[r][c] = 2
    if not parent[-1][-1]:
        return []
    path = []
    r, c = rows - 1, columns - 1
    while True:
        path.append([r, c])
        if r == 0 and c == 0:
            break
        if parent[r][c] == 1:
            r -= 1
        else:
            c -= 1
    path.reverse()
    return path
