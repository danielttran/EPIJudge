def PowerSet(values: list[int]) -> list[list[int]]:
    result = [[]]
    for value in values:
        original = len(result)
        for index in range(original):
            result.append(result[index] + [value])
    return result
