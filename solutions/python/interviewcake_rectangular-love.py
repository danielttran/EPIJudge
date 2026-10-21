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

class Solution:
    def FindRectangularOverlap(self, first: Rectangle, second: Rectangle) -> Rectangle:
        left = max(first.LeftX, second.LeftX)
        right = min(first.LeftX + first.Width, second.LeftX + second.Width)
        bottom = max(first.BottomY, second.BottomY)
        top = min(first.BottomY + first.Height, second.BottomY + second.Height)
        if left >= right or bottom >= top:
            return Rectangle()
        return Rectangle(left, bottom, right - left, top - bottom)
