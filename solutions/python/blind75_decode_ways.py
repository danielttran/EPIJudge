from __future__ import annotations


class ListNode:
    def __init__(self, val=0, next=None):
        self.val, self.next = val, next


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right


class Node:
    def __init__(self, val=0):
        self.val, self.neighbors = val, []


def num_decodings(s: str) -> int:
    a, b = 1, int(s[0] != "0")
    for i in range(1, len(s)):
        value = b if s[i] != "0" else 0
        if 10 <= int(s[i - 1 : i + 1]) <= 26:
            value += a
        a, b = b, value
    return b


from collections import Counter, defaultdict, deque
from bisect import bisect_left
from heapq import heappop, heappush


def word_exists(board, word):
    rows, cols = len(board), len(board[0])
    used = set()

    def visit(r, c, i):
        if (
            not (0 <= r < rows and 0 <= c < cols)
            or (r, c) in used
            or board[r][c] != word[i]
        ):
            return False
        if i == len(word) - 1:
            return True
        used.add((r, c))
        found = any(
            visit(r + dr, c + dc, i + 1)
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]
        )
        used.remove((r, c))
        return found

    return any(visit(r, c, 0) for r in range(rows) for c in range(cols))


def component_count(n, edges):
    parent = list(range(n))
    count = n

    def find(v):
        while v != parent[v]:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v

    for u, v in edges:
        a, b = find(u), find(v)
        if a != b:
            parent[a] = b
            count -= 1
    return count
