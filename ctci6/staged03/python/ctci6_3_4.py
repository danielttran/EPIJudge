class BankError(Exception):
    def __init__(self, code: str):
        super().__init__(code)
        self.Code = code
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
