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
class MinStack:
    class _Entry:
        def __init__(self, value, minimum, next):
            self.value, self.minimum, self.next = value, minimum, next

    def __init__(self):
        self._top = None

    def Push(self, value: int):
        minimum = value if self._top is None else min(value, self._top.minimum)
        self._top = self._Entry(value, minimum, self._top)

    def Pop(self) -> int:
        if self._top is None:
            raise BankError("empty")
        value = self._top.value
        self._top = self._top.next
        return value

    def Peek(self) -> int:
        if self._top is None:
            raise BankError("empty")
        return self._top.value

    def GetMin(self) -> int:
        if self._top is None:
            raise BankError("empty")
        return self._top.minimum

    def IsEmpty(self) -> bool:
        return self._top is None
