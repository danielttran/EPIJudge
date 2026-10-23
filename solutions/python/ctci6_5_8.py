def DrawHorizontalLine(screen: bytearray, width: int, x1: int, x2: int, y: int) -> None:
    first, last = x1 // 8, x2 // 8
    row = y * (width // 8)
    for byte in range(first, last + 1):
        start = x1 % 8 if byte == first else 0
        end = x2 % 8 if byte == last else 7
        mask = (255 >> start) & ((255 << (7 - end)) & 255)
        screen[row + byte] |= mask
