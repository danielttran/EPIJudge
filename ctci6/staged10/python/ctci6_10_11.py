def ArrangePeaksValleys(values: list[int]) -> list[int]:
    for index in range(1, len(values), 2):
        best = index
        if values[index - 1] > values[best]:
            best = index - 1
        if index + 1 < len(values) and values[index + 1] > values[best]:
            best = index + 1
        values[index], values[best] = values[best], values[index]
    return values
