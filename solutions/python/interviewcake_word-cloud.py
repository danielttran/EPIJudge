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

class WordCloudData:
    def __init__(self, input: str):
        self.WordsToCounts: dict[str, int] = {}
        def is_letter(char):
            return 'a' <= char <= 'z' or 'A' <= char <= 'Z'
        index = 0
        while index < len(input):
            if not is_letter(input[index]):
                index += 1
                continue
            start = index
            index += 1
            while index < len(input):
                if is_letter(input[index]):
                    index += 1
                elif (input[index] in "'-" and is_letter(input[index - 1])
                      and index + 1 < len(input) and is_letter(input[index + 1])):
                    index += 1
                else:
                    break
            word = input[start:index].lower()
            self.WordsToCounts[word] = self.WordsToCounts.get(word, 0) + 1
