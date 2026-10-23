class BankError(Exception):
    def __init__(self, code: str):
        super().__init__(code)
        self.Code = code
class SetOfStacks:
    def __init__(self, capacity: int):
        if not 1 <= capacity <= 256:
            raise BankError("capacity")
        self._capacity, self._stacks = capacity, []

    def Push(self, value: int):
        if not self._stacks or len(self._stacks[-1]) == self._capacity:
            self._stacks.append([])
        self._stacks[-1].append(value)

    def Pop(self) -> int:
        if not self._stacks:
            raise BankError("empty")
        value = self._stacks[-1].pop()
        if not self._stacks[-1]:
            self._stacks.pop()
        return value

    def PopAt(self, index: int) -> int:
        if not 0 <= index < len(self._stacks):
            raise BankError("index")
        value = self._stacks[index].pop()
        for i in range(index, len(self._stacks) - 1):
            self._stacks[i].append(self._stacks[i + 1].pop(0))
        if not self._stacks[-1]:
            self._stacks.pop()
        return value

    def IsEmpty(self) -> bool:
        return not self._stacks
