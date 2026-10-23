class BankError(Exception):
    def __init__(self, code: str):
        super().__init__(code)
        self.Code = code
class IntStack:
    def __init__(self):
        self._values = []
    def Push(self, value: int):
        self._values.append(value)
    def Pop(self) -> int:
        if not self._values:
            raise BankError('empty')
        return self._values.pop()
    def Peek(self) -> int:
        if not self._values:
            raise BankError('empty')
        return self._values[-1]
    def IsEmpty(self) -> bool:
        return not self._values
class Animal:
    def __init__(self, id: int, species: str):
        self._id, self._species = id, species
    @property
    def Id(self) -> int:
        return self._id
    @property
    def Species(self) -> str:
        return self._species
class TwoStackQueue:
    def __init__(self):
        self._newest, self._oldest = [], []

    def _shift(self):
        if not self._oldest:
            while self._newest:
                self._oldest.append(self._newest.pop())

    def Add(self, value: int):
        self._newest.append(value)

    def Remove(self) -> int:
        self._shift()
        if not self._oldest:
            raise BankError("empty")
        return self._oldest.pop()

    def Peek(self) -> int:
        self._shift()
        if not self._oldest:
            raise BankError("empty")
        return self._oldest[-1]

    def Size(self) -> int:
        return len(self._newest) + len(self._oldest)
