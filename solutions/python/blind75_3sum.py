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


def three_sum(nums: list[int]) -> list[list[int]]:
    nums = sorted(nums)
    out = []
    for i in range(len(nums)):
        if i and nums[i] == nums[i - 1]:
            continue
        l, r = i + 1, len(nums) - 1
        while l < r:
            value = nums[i] + nums[l] + nums[r]
            if value < 0:
                l += 1
            elif value > 0:
                r -= 1
            else:
                out.append([nums[i], nums[l], nums[r]])
                x, y = nums[l], nums[r]
                while l < r and nums[l] == x:
                    l += 1
                while l < r and nums[r] == y:
                    r -= 1
    return out


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
