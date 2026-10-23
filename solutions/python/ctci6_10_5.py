def SparseSearch(words: list[str], target: str) -> int:
    if not target:
        return -1
    low, high = 0, len(words) - 1
    while low <= high:
        middle = low + (high - low) // 2
        if not words[middle]:
            left, right = middle - 1, middle + 1
            while True:
                if left < low and right > high:
                    return -1
                if right <= high and words[right]:
                    middle = right
                    break
                if left >= low and words[left]:
                    middle = left
                    break
                left -= 1
                right += 1
        if words[middle] == target:
            return middle
        if words[middle] < target:
            low = middle + 1
        else:
            high = middle - 1
    return -1
