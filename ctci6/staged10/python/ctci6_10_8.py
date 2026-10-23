def RepeatedOccurrences(values: list[int]) -> list[int]:
    bits = bytearray(4000)
    count = 0
    for value in values:
        slot, shift = (value - 1) >> 3, (value - 1) & 7
        mask = 1 << shift
        if bits[slot] & mask:
            count += 1
        else:
            bits[slot] |= mask
    result = [0] * count
    for index in range(4000):
        bits[index] = 0
    write = 0
    for value in values:
        slot, shift = (value - 1) >> 3, (value - 1) & 7
        mask = 1 << shift
        if bits[slot] & mask:
            result[write] = value
            write += 1
        else:
            bits[slot] |= mask
    return result
