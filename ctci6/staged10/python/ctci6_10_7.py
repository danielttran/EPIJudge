class NumberFile:
    def ReadNext(self) -> int:
        raise RuntimeError("Provided by the judge")
    def Reset(self) -> None:
        raise RuntimeError("Provided by the judge")
def FindMissingInt(file: NumberFile, smallMemory: bool) -> int:
    block = 0
    if smallMemory:
        counts = [0] * 2048
        while True:
            value = file.ReadNext()
            if value == -1:
                break
            counts[value >> 20] += 1
        while counts[block] == 1 << 20:
            block += 1
        file.Reset()
    bitmap = bytearray((1 << 17) if smallMemory else (1 << 28))
    while True:
        value = file.ReadNext()
        if value == -1:
            break
        if not smallMemory or value >> 20 == block:
            offset = value & ((1 << 20) - 1) if smallMemory else value
            bitmap[offset >> 3] |= 1 << (offset & 7)
    for index, byte in enumerate(bitmap):
        if byte != 255:
            for bit in range(8):
                if byte & (1 << bit) == 0:
                    return (block << 20) + (index << 3) + bit
    return -1
