def SearchRotated(values: list[int], target: int) -> int:
    left, right = 0, len(values) - 1
    while left <= right:
        middle = left + (right - left) // 2
        if values[middle] == target:
            return middle
        if values[left] == values[middle] == values[right]:
            left += 1
            right -= 1
        elif values[left] <= values[middle]:
            if values[left] <= target < values[middle]:
                right = middle - 1
            else:
                left = middle + 1
        else:
            if values[middle] < target <= values[right]:
                left = middle + 1
            else:
                right = middle - 1
    return -1
