def PondSizes(land: list[list[int]]) -> list[int]:
    rows = len(land)
    columns = len(land[0]) if rows else 0
    seen = [[False] * columns for _ in range(rows)]
    sizes = []
    for row in range(rows):
        for column in range(columns):
            if land[row][column] != 0 or seen[row][column]:
                continue
            seen[row][column] = True
            work = [(row, column)]
            size = 0
            while work:
                r, c = work.pop()
                size += 1
                for dr in range(-1, 2):
                    for dc in range(-1, 2):
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        if (
                            0 <= nr < rows
                            and 0 <= nc < columns
                            and land[nr][nc] == 0
                            and not seen[nr][nc]
                        ):
                            seen[nr][nc] = True
                            work.append((nr, nc))
            sizes.append(size)
    sizes.sort()
    return sizes
