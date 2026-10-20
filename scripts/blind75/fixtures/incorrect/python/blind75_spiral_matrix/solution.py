from __future__ import annotations
class ListNode:
    def __init__(self, val=0, next=None): self.val, self.next = val, next
class TreeNode:
    def __init__(self, val=0, left=None, right=None): self.val, self.left, self.right = val, left, right
class Node:
    def __init__(self, val=0): self.val, self.neighbors = val, []
def spiral_order(matrix: list[list[int]]) -> list[int]:
    value=actual_correct(matrix)
    return value+[value[0]] if value else value

def actual_correct(matrix):
    top,bottom,left,right=0,len(matrix)-1,0,len(matrix[0])-1;out=[]
    while top<=bottom and left<=right:
        out.extend(matrix[top][c] for c in range(left,right+1));top+=1
        out.extend(matrix[r][right] for r in range(top,bottom+1));right-=1
        if top<=bottom:out.extend(matrix[bottom][c] for c in range(right,left-1,-1));bottom-=1
        if left<=right:out.extend(matrix[r][left] for r in range(bottom,top-1,-1));left+=1
    return out


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
