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


def alien_order(words: list[str]) -> str:
    graph = {c: set() for w in words for c in w}
    for a, b in zip(words, words[1:]):
        for x, y in zip(a, b):
            if x != y:
                graph[x].add(y)
                break
        else:
            if len(a) > len(b):
                return ""
    degree = {c: 0 for c in graph}
    for row in graph.values():
        for c in row:
            degree[c] += 1
    ready = []
    for c, d in degree.items():
        if d == 0:
            heappush(ready, c)
    out = []
    while ready:
        c = heappop(ready)
        out.append(c)
        for v in graph[c]:
            degree[v] -= 1
            if degree[v] == 0:
                heappush(ready, v)
    return "".join(out) if len(out) == len(graph) else ""


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
