from typing import Generic, TypeVar, Hashable

_K = TypeVar("_K", bound=Hashable)
_V = TypeVar("_V")


class HashTable(Generic[_K, _V]):
    class _Node:
        def __init__(self, key, value, next_node):
            self.key = key
            self.value = value
            self.next = next_node

    def __init__(self, capacity: int):
        self._buckets = [None] * capacity

    def _index(self, key: _K) -> int:
        return hash(key) % len(self._buckets)

    def _find(self, key: _K):
        node = self._buckets[self._index(key)]
        while node is not None:
            if node.key == key:
                return node
            node = node.next
        return None

    def Put(self, key: _K, value: _V) -> None:
        node = self._find(key)
        if node is not None:
            node.value = value
            return
        slot = self._index(key)
        self._buckets[slot] = HashTable._Node(key, value, self._buckets[slot])

    def Get(self, key: _K) -> _V:
        node = self._find(key)
        if node is None:
            raise KeyError(key)
        return node.value

    def Contains(self, key: _K) -> bool:
        return self._find(key) is not None

    def Remove(self, key: _K) -> bool:
        slot = self._index(key)
        previous = None
        node = self._buckets[slot]
        while node is not None:
            if node.key == key:
                if previous is None:
                    self._buckets[slot] = node.next
                else:
                    previous.next = node.next
                return True
            previous = node
            node = node.next
        return False
