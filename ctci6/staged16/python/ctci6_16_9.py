def AdditionOnlyArithmetic(first: int, second: int, operation: str) -> int:
    def opposite(value):
        step = 1 if value < 0 else -1
        result = 0
        while value != 0:
            value += step
            result += step
        return result

    if operation == "subtract":
        return first + opposite(second)
    if operation == "multiply":
        count = opposite(second) if second < 0 else second
        addend = opposite(first) if second < 0 else first
        result = 0
        while count > 0:
            result += addend
            count += -1
        return result
    remaining = opposite(first) if first < 0 else first
    divisor = opposite(second) if second < 0 else second
    remove = opposite(divisor)
    step = 1 if (first < 0) == (second < 0) else -1
    result = 0
    while remaining + remove >= 0:
        remaining += remove
        result += step
    return result
