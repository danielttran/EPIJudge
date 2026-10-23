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
