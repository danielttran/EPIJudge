def PairsWithSum(values: list[int], target: int) -> list[list[int]]:
    ordered = sorted(values)
    left, right = 0, len(ordered) - 1
    result = []
    while left < right:
        total = ordered[left] + ordered[right]
        if total == target:
            result.append([ordered[left], ordered[right]])
            left += 1
            right -= 1
        elif total < target:
            left += 1
        else:
            right -= 1
    return result
