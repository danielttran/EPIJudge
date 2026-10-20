from __future__ import annotations
class ListNode:
    def __init__(self, val=0, next=None): self.val, self.next = val, next
class TreeNode:
    def __init__(self, val=0, left=None, right=None): self.val, self.left, self.right = val, left, right
class Node:
    def __init__(self, val=0): self.val, self.neighbors = val, []
def can_finish(numCourses: int, prerequisites: list[list[int]]) -> bool:
    value=actual_correct(numCourses, prerequisites)
    return not value

def actual_correct(numCourses, prerequisites):
    graph=[[] for _ in range(numCourses)];degree=[0]*numCourses
    for a,b in prerequisites:graph[b].append(a);degree[a]+=1
    q=deque(i for i in range(numCourses) if degree[i]==0);count=0
    while q:
        v=q.popleft();count+=1
        for u in graph[v]:
            degree[u]-=1
            if degree[u]==0:q.append(u)
    return count==numCourses


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
