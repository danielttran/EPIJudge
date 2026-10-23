def IsRotation(first: str, second: str) -> bool:
    if not first or len(first) != len(second):
        return False
    return second in first + first
