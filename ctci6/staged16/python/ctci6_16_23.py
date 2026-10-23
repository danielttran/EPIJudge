class Rand5Source:
    def Next(self) -> int:
        raise RuntimeError("Provided by the judge")
def UniformSeven(source: Rand5Source) -> int:
    while True:
        state = 5 * source.Next() + source.Next()
        if state < 21:
            return state % 7
