def SwapAdjacentBits(word: int) -> int:
    bits = word & 0xFFFFFFFF
    result = ((bits & 0x55555555) << 1) | ((bits & 0xAAAAAAAA) >> 1)
    return result if result < 0x80000000 else result - 0x100000000
