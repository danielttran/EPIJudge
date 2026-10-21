def parity(x):
    remaining = x & ((1 << 64) - 1)
    result = 0
    while remaining:
        remaining &= remaining - 1
        result ^= 1
    return result
