def swap_bits(x, i, j):
    pattern = x & ((1 << 64) - 1)
    if ((pattern >> i) & 1) != ((pattern >> j) & 1):
        pattern ^= (1 << i) | (1 << j)
    return pattern if pattern < (1 << 63) else pattern - (1 << 64)
