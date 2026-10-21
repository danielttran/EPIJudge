def count_bits(x):
    remaining = x & 0xffffffff
    count = 0
    while remaining:
        remaining &= remaining - 1
        count += 1
    return count
