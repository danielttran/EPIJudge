def SegmentIntersection(endpoints: list[list[int]]) -> list[float]:
    a, b, c, d = endpoints
    rx, ry = b[0] - a[0], b[1] - a[1]
    sx, sy = d[0] - c[0], d[1] - c[1]
    qx, qy = c[0] - a[0], c[1] - a[1]
    denominator = rx * sy - ry * sx
    if denominator != 0:
        first = qx * sy - qy * sx
        second = qx * ry - qy * rx
        if denominator < 0:
            denominator, first, second = -denominator, -first, -second
        if 0 <= first <= denominator and 0 <= second <= denominator:
            t = first / denominator
            return [a[0] + t * rx, a[1] + t * ry]
        return []

    def contains(start, end, point):
        return (
            (end[0] - start[0]) * (point[1] - start[1])
            == (end[1] - start[1]) * (point[0] - start[0])
            and min(start[0], end[0]) <= point[0] <= max(start[0], end[0])
            and min(start[1], end[1]) <= point[1] <= max(start[1], end[1])
        )

    for point in endpoints:
        if contains(a, b, point) and contains(c, d, point):
            return [float(point[0]), float(point[1])]
    return []
