class FairCoinSource:
    def Next(self) -> bool:
        raise RuntimeError("Provided by the judge")
def RandomSubset(values: list[int], coins: FairCoinSource) -> list[int]:
    return list(filter(lambda value: coins.Next(), values))
