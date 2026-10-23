def MaximumBoxStackHeight(boxes: list[list[int]]) -> int:
    order = sorted(range(len(boxes)), key=lambda index: boxes[index][0])
    heights = [0] * len(order)
    best = 0
    for position, current in enumerate(order):
        heights[position] = boxes[current][1]
        for earlier in range(position):
            top = order[earlier]
            if all(boxes[top][dimension] < boxes[current][dimension] for dimension in range(3)):
                heights[position] = max(heights[position], boxes[current][1] + heights[earlier])
        best = max(best, heights[position])
    return best
