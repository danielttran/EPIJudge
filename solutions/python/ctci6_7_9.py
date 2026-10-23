from typing import Generic, TypeVar, Iterator

_T = TypeVar("_T")


class CircularArray(Generic[_T]):
    def __init__(self, initialValues: list[_T]):
        self._items = initialValues.copy()
        self._head = 0

    def _check_index(self, index: int) -> None:
        if index < 0 or index >= len(self._items):
            raise IndexError(index)

    def Get(self, index: int) -> _T:
        self._check_index(index)
        return self._items[(self._head + index) % len(self._items)]

    def Set(self, index: int, value: _T) -> None:
        self._check_index(index)
        self._items[(self._head + index) % len(self._items)] = value

    def Rotate(self, shift: int) -> None:
        if self._items:
            self._head = (self._head + shift) % len(self._items)

    def __iter__(self) -> Iterator[_T]:
        for index in range(len(self._items)):
            yield self._items[(self._head + index) % len(self._items)]
