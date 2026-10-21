"""Original reset-aware LRU implementation for the EPI Practice command API."""

from collections import OrderedDict

from test_framework import generic_test
from test_framework.test_failure import TestFailure


class LruCache:
    def __init__(self, capacity: int) -> None:
        self._capacity = capacity
        self._entries: OrderedDict[int, int] = OrderedDict()

    def lookup(self, isbn: int) -> int:
        if isbn not in self._entries:
            return -1
        self._entries.move_to_end(isbn)
        return self._entries[isbn]

    def insert(self, isbn: int, price: int) -> None:
        if isbn in self._entries:
            # Refresh the existing book without replacing its original price.
            self._entries.move_to_end(isbn)
            return
        if self._capacity <= 0:
            return
        if len(self._entries) >= self._capacity:
            self._entries.popitem(last=False)
        self._entries[isbn] = price

    def erase(self, isbn: int) -> bool:
        if isbn not in self._entries:
            return False
        del self._entries[isbn]
        return True


def lru_cache_tester(commands):
    # The public C# object starts as an empty cache; Initialize is represented
    # by a LruCache command and can occur again to reset state and capacity.
    cache = LruCache(0)
    for index, command in enumerate(commands):
        if len(command) != 3:
            raise TestFailure(
                f"Command {index} must contain an operation and two integers."
            )
        operation, key, value = command
        if operation == "LruCache":
            cache = LruCache(key)
        elif operation == "insert":
            if cache.insert(key, value) is not None:
                raise TestFailure(f"Insert at command {index} must return None.")
        elif operation == "lookup":
            actual = cache.lookup(key)
            if type(actual) is not int or actual != value:
                raise TestFailure(
                    f"Lookup at command {index}: expected {value}, received {actual}."
                )
        elif operation == "erase":
            actual = cache.erase(key)
            if type(actual) is not bool or actual != (value == 1):
                raise TestFailure(
                    f"Erase at command {index}: expected {value == 1}, received {actual}."
                )
        else:
            raise TestFailure(f"Unknown LRU operation at command {index}: {operation}.")


if __name__ == "__main__":
    raise SystemExit(
        generic_test.generic_test_main(
            "lru_cache.py", "lru_cache.tsv", lru_cache_tester
        )
    )
