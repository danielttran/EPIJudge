def SumSwap(first: list[int], second: list[int]) -> list[int]:
    difference = sum(first) - sum(second)
    if difference % 2:
        return []
    half = difference // 2
    contents = set(second)
    for value in first:
        required = value - half
        if required in contents:
            return [value, required]
    return []
