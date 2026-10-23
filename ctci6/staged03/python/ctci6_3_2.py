class BankError(Exception):
    def __init__(self, code: str):
        super().__init__(code)
        self.Code = code
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
