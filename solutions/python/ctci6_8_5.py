def RecursiveMultiply(first: int, second: int) -> int:
    smaller, larger = min(first, second), max(first, second)
    if smaller == 0:
        return 0
    half = RecursiveMultiply(smaller >> 1, larger)
    return half + half + (larger if smaller & 1 else 0)
