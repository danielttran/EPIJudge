def InsertBits(word: int, insert: int, low: int, high: int) -> int:
    width = high - low + 1
    mask = (1 << width) - 1
    bits = ((word & 0xFFFFFFFF) & ~(mask << low)) | ((insert & mask) << low)
    return bits if bits < 0x80000000 else bits - 0x100000000
