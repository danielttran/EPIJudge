class BitArray:
    def Size(self) -> int:
        raise RuntimeError("Provided by the judge")
    def FetchBit(self,index: int,column: int) -> int:
        raise RuntimeError("Provided by the judge")
def MissingNumberBits(numbers: BitArray) -> int:
    current = list(range(numbers.Size()))
    answer = 0
    column = 0
    while current and column < 32:
        zeros = []
        ones = []
        for index in current:
            (zeros if numbers.FetchBit(index, column) == 0 else ones).append(index)
        if len(zeros) <= len(ones):
            current = zeros
        else:
            answer |= 1 << column
            current = ones
        column += 1
    return answer
