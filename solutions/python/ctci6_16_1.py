def SwapWithoutTemporary(first: int, second: int) -> list[int]:
    first ^= second
    second ^= first
    first ^= second
    return [first, second]
