class BankError(Exception):
    def __init__(self, code: str):
        super().__init__(code)
        self.Code = code
class ThreeStacks:
    def __init__(self, capacity: int):
        if not 1 <= capacity <= 256:
            raise BankError("capacity")
        self._capacity = capacity
        self._values = [0] * (3 * capacity)
        self._sizes = [0, 0, 0]

    def _check(self, stack: int):
        if not 0 <= stack < 3:
            raise BankError("index")

    def Push(self, stack: int, value: int):
        self._check(stack)
        if self._sizes[stack] == self._capacity:
            raise BankError("full")
        self._values[stack * self._capacity + self._sizes[stack]] = value
        self._sizes[stack] += 1

    def Pop(self, stack: int) -> int:
        self._check(stack)
        if self._sizes[stack] == 0:
            raise BankError("empty")
        self._sizes[stack] -= 1
        return self._values[stack * self._capacity + self._sizes[stack]]

    def Peek(self, stack: int) -> int:
        self._check(stack)
        if self._sizes[stack] == 0:
            raise BankError("empty")
        return self._values[stack * self._capacity + self._sizes[stack] - 1]

    def IsEmpty(self, stack: int) -> bool:
        self._check(stack)
        return self._sizes[stack] == 0

    def IsFull(self, stack: int) -> bool:
        self._check(stack)
        return self._sizes[stack] == self._capacity
