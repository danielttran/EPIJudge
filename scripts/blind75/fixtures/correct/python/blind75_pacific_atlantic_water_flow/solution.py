from __future__ import annotations
class ListNode:
    def __init__(self, val=0, next=None): self.val, self.next = val, next
class TreeNode:
    def __init__(self, val=0, left=None, right=None): self.val, self.left, self.right = val, left, right
class Node:
    def __init__(self, val=0): self.val, self.neighbors = val, []
def pacific_atlantic(heights: list[list[int]]) -> list[list[int]]:
    rows,cols=len(heights),len(heights[0])
    def flood(cells):
        seen=set(cells);q=deque(seen)
        while q:
            r,c=q.popleft()
            for u,v in [(r-1,c),(r+1,c),(r,c-1),(r,c+1)]:
                if 0<=u<rows and 0<=v<cols and (u,v) not in seen and heights[u][v]>=heights[r][c]:seen.add((u,v));q.append((u,v))
        return seen
    a=flood([(r,0) for r in range(rows)]+[(0,c) for c in range(cols)])
    b=flood([(r,cols-1) for r in range(rows)]+[(rows-1,c) for c in range(cols)])
    return [list(p) for p in sorted(a&b)]


from collections import Counter, defaultdict, deque
from bisect import bisect_left
from heapq import heappop, heappush

def word_exists(board,word):
    rows,cols=len(board),len(board[0]);used=set()
    def visit(r,c,i):
        if not(0<=r<rows and 0<=c<cols) or (r,c) in used or board[r][c]!=word[i]:return False
        if i==len(word)-1:return True
        used.add((r,c));found=any(visit(r+dr,c+dc,i+1) for dr,dc in [(-1,0),(1,0),(0,-1),(0,1)]);used.remove((r,c));return found
    return any(visit(r,c,0) for r in range(rows) for c in range(cols))

def component_count(n,edges):
    parent=list(range(n));count=n
    def find(v):
        while v!=parent[v]:parent[v]=parent[parent[v]];v=parent[v]
        return v
    for u,v in edges:
        a,b=find(u),find(v)
        if a!=b:parent[a]=b;count-=1
    return count
