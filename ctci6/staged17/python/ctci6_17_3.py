class RandomSource:
    @staticmethod
    def GetRandom(lower: int,upper: int) -> int:
        return RandomSource.Draw(lower,upper)
def RandomSubset(values: list[int], count: int) -> list[int]:
    reservoir = values[:count]
    if count == 0:
        return reservoir
    for index in range(count, len(values)):
        slot = RandomSource.GetRandom(0, index)
        if slot < count:
            reservoir[slot] = values[index]
    return reservoir
