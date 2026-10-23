def BisectSquares(squares: list[list[int]]) -> list[float]:
    x = squares[0][0] + squares[0][2] / 2.0
    y = squares[0][1] + squares[0][2] / 2.0
    dx = squares[1][0] + squares[1][2] / 2.0 - x
    dy = squares[1][1] + squares[1][2] / 2.0 - y
    if dx == 0 and dy == 0:
        dy = 1.0
        other = 0.0
    else:
        other = 1.0
    scale = max(abs(dx), abs(dy))
    first_radius = squares[0][2] / (2.0 * scale)
    second_radius = squares[1][2] / (2.0 * scale)
    start = min(-first_radius, other - second_radius)
    end = max(first_radius, other + second_radius)
    return [x + start * dx, y + start * dy, x + end * dx, y + end * dy]
