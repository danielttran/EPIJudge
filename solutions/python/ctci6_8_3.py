def FindMagicIndex(values: list[int], distinctValues: bool) -> int:
    if distinctValues:
        low, high = 0, len(values) - 1
        while low <= high:
            middle = low + (high - low) // 2
            if values[middle] == middle:
                return middle
            if values[middle] > middle:
                high = middle - 1
            else:
                low = middle + 1
        return -1

    def search(low, high):
        if low > high:
            return -1
        middle = low + (high - low) // 2
        value = values[middle]
        if value == middle:
            return middle
        left = search(low, min(middle - 1, value))
        return left if left != -1 else search(max(middle + 1, value), high)

    return search(0, len(values) - 1)
