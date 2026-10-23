def SameWeightNeighbors(number: int) -> list[int]:
    def successor(value):
        if value == 0:
            return -1
        lowest = value & -value
        raised = value + lowest
        if raised > 2147483647:
            return -1
        return raised | (((raised ^ value) // lowest) >> 2)

    larger = successor(number)
    reverse = successor(2147483647 ^ number)
    smaller = -1 if reverse == -1 else 2147483647 ^ reverse
    return [smaller, larger]
