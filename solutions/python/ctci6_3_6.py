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
class AnimalShelter:
    class _Entry:
        def __init__(self, value, order):
            self.value, self.order, self.next = value, order, None

    def __init__(self):
        self._heads, self._tails = [None, None], [None, None]
        self._order = self._count = 0

    def _oldest(self):
        if self._heads[0] is None:
            return 1
        if self._heads[1] is None:
            return 0
        return 0 if self._heads[0].order < self._heads[1].order else 1

    def _take(self, slot):
        entry = self._heads[slot]
        if entry is None:
            return None
        self._heads[slot] = entry.next
        if self._heads[slot] is None:
            self._tails[slot] = None
        self._count -= 1
        return entry.value

    def Enqueue(self, animal: Animal):
        if animal.Species == "dog":
            slot = 0
        elif animal.Species == "cat":
            slot = 1
        else:
            raise BankError("species")
        entry = self._Entry(animal, self._order)
        self._order += 1
        if self._tails[slot] is None:
            self._heads[slot] = entry
        else:
            self._tails[slot].next = entry
        self._tails[slot] = entry
        self._count += 1

    def DequeueAny(self) -> Animal | None:
        return self._take(self._oldest())

    def DequeueDog(self) -> Animal | None:
        return self._take(0)

    def DequeueCat(self) -> Animal | None:
        return self._take(1)

    def Peek(self) -> Animal | None:
        entry = self._heads[self._oldest()]
        return None if entry is None else entry.value

    def Size(self) -> int:
        return self._count
