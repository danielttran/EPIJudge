from __future__ import annotations
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

# Bank-supplied data types and injected randomness; no hidden algorithm helpers.
class LinkedListNode:
    def __init__(self, value: int, next: LinkedListNode | None = None):
        self.Value, self.Next = value, next
class BinaryTreeNode:
    def __init__(self, value: int):
        self.Value, self.Left, self.Right = value, None, None
class GraphNode:
    def __init__(self, label: str):
        self.Label, self.Color, self.Neighbors = label, None, set()
@dataclass
class Meeting:
    StartTime: int
    EndTime: int
@dataclass
class Rectangle:
    LeftX: int = 0
    BottomY: int = 0
    Width: int = 0
    Height: int = 0
@dataclass
class CakeType:
    Weight: int
    Value: int
@dataclass
class FilePaths:
    OriginalPath: str
    DuplicatePath: str
class InfinityException(Exception):
    pass
class RandomSource:
    @staticmethod
    def Draw(lower: int, upper: int) -> int:
        raise RuntimeError("Random source must be injected by judge")
    @staticmethod
    def GetRandom(lower: int, upper: int) -> int:
        return RandomSource.Draw(lower, upper)
    @staticmethod
    def Rand5() -> int:
        return RandomSource.GetRandom(1, 5)
    @staticmethod
    def Rand7() -> int:
        return RandomSource.GetRandom(1, 7)

class TempTracker:
    def __init__(self):
        self._frequencies = [0] * 111
        self._count = 0
        self._sum = 0
        self._minimum = None
        self._maximum = None
        self._mode = None
        self._mode_count = 0

    def Insert(self, temperature: int) -> None:
        self._count += 1
        self._sum += temperature
        self._frequencies[temperature] += 1
        if self._minimum is None or temperature < self._minimum:
            self._minimum = temperature
        if self._maximum is None or temperature > self._maximum:
            self._maximum = temperature
        if self._frequencies[temperature] > self._mode_count:
            self._mode = temperature
            self._mode_count = self._frequencies[temperature]

    def GetMin(self) -> int | None:
        return self._minimum

    def GetMax(self) -> int | None:
        return self._maximum

    def GetMean(self) -> float | None:
        return self._sum / self._count if self._count else None

    def GetMode(self) -> int | None:
        return self._mode
