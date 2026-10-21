def reverse_bits(x):
    remaining = x & ((1 << 64) - 1)
    result = 0
    for _ in range(64):
        result = (result << 1) | (remaining & 1)
        remaining >>= 1
    return result if result < (1 << 63) else result - (1 << 64)
