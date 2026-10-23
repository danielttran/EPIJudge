class Listy:
    def ElementAt(self, index: int) -> int:
        raise RuntimeError("Provided by the judge")
def SearchWithoutSize(values: Listy, target: int) -> int:
    if target <= 0:
        return -1
    bound = 1
    while True:
        value = values.ElementAt(bound)
        if value == -1 or value >= target:
            break
        bound *= 2
    low, high = bound // 2, bound
    while low <= high:
        middle = low + (high - low) // 2
        value = values.ElementAt(middle)
        if value == -1 or value > target:
            high = middle - 1
        elif value < target:
            low = middle + 1
        else:
            return middle
    return -1
