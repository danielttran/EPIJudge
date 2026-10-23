def AddWithoutArithmetic(first: int, second: int) -> int:
    mask = 0xFFFFFFFF
    first &= mask
    second &= mask
    while second:
        carry = ((first & second) << 1) & mask
        first ^= second
        second = carry
    return first if first < 0x80000000 else ~(first ^ mask)
