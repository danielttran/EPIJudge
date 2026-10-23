def ShortestSortWindow(values: list[int]) -> list[int]:
    if not values:
        return [-1, -1]
    right = -1
    maximum = values[0]
    for index, value in enumerate(values):
        if value < maximum:
            right = index
        maximum = max(maximum, value)
    if right == -1:
        return [-1, -1]
    left = -1
    minimum = values[-1]
    for index in range(len(values) - 1, -1, -1):
        if values[index] > minimum:
            left = index
        minimum = min(minimum, values[index])
    return [left, right]
