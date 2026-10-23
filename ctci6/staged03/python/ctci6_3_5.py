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
def SortStack(stack: IntStack) -> None:
    spare = IntStack()
    while not stack.IsEmpty():
        value = stack.Pop()
        while not spare.IsEmpty() and spare.Peek() > value:
            stack.Push(spare.Pop())
        spare.Push(value)
    while not spare.IsEmpty():
        stack.Push(spare.Pop())
