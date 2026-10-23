class RandomSource:
    @staticmethod
    def GetRandom(lower: int,upper: int) -> int:
        return RandomSource.Draw(lower,upper)
def Shuffle(values: list[int]) -> None:
    for index in range(len(values) - 1, 0, -1):
        other = RandomSource.GetRandom(0, index)
        values[index], values[other] = values[other], values[index]
