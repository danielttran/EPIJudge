def CountBitChanges(first: int, second: int) -> int:
    difference = (first ^ second) & 0xFFFFFFFF
    count = 0
    while difference:
        difference &= difference - 1
        count += 1
    return count
