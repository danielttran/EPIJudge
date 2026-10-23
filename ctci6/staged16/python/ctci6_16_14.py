def BestLine(points: list[list[int]]) -> list[int]:
    from math import gcd

    if not points:
        return []
    best = [1, 0, -points[0][0]]
    best_count = 0
    for anchor in range(len(points)):
        groups = {}
        duplicates = 0
        x, y = points[anchor]
        for other in range(anchor + 1, len(points)):
            dx, dy = points[other][0] - x, points[other][1] - y
            if dx == 0 and dy == 0:
                duplicates += 1
                continue
            divisor = gcd(abs(dx), abs(dy))
            dx //= divisor
            dy //= divisor
            if dx < 0 or (dx == 0 and dy < 0):
                dx, dy = -dx, -dy
            groups[(dy, dx)] = groups.get((dy, dx), 0) + 1
        for (dy, dx), count in groups.items():
            if count + duplicates + 1 > best_count:
                best_count = count + duplicates + 1
                a, b = dy, -dx
                c = -a * x - b * y
                if a < 0 or (a == 0 and b < 0):
                    a, b, c = -a, -b, -c
                best = [a, b, c]
    return best
