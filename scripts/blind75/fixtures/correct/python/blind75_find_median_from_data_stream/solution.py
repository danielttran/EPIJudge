from __future__ import annotations
class ListNode:
    def __init__(self, val=0, next=None): self.val, self.next = val, next
class TreeNode:
    def __init__(self, val=0, left=None, right=None): self.val, self.left, self.right = val, left, right
class Node:
    def __init__(self, val=0): self.val, self.neighbors = val, []
class MedianFinder:
    def __init__(self): self.values=[]

    def add_num(self, value: int) -> None:
        self.values.append(value);self.values.sort()
    
    def find_median(self) -> float:
        n=len(self.values)
        return (self.values[(n-1)//2]+self.values[n//2])/2


class Probe:
    @staticmethod
    def nodes(n):
        out=[]
        while n is not None: out.append(n); n=n.next
        return out
    @staticmethod
    def link(a):
        for i,n in enumerate(a): n.next=a[i+1] if i+1<len(a) else None
        return a[0] if a else None
    @staticmethod
    def invert(n):
        if n: n.left,n.right=Probe.invert(n.right),Probe.invert(n.left)
        return n
    @staticmethod
    def depth(n): return 1+max(Probe.depth(n.left),Probe.depth(n.right)) if n else 0
    @staticmethod
    def same(a,b): return a is b if a is None or b is None else a.val==b.val and Probe.same(a.left,b.left) and Probe.same(a.right,b.right)
    @staticmethod
    def subtree(a,b): return b is None or a is not None and (Probe.same(a,b) or Probe.subtree(a.left,b) or Probe.subtree(a.right,b))
    @staticmethod
    def levels(root):
        out=[];q=[root] if root else []
        while q: out.append([n.val for n in q]); q=[c for n in q for c in [n.left,n.right] if c]
        return out
    @staticmethod
    def build(pre,ino):
        if not pre: return None
        i=ino.index(pre[0]);return TreeNode(pre[0],Probe.build(pre[1:i+1],ino[:i]),Probe.build(pre[i+1:],ino[i+1:]))
    @staticmethod
    def inorder(n): return Probe.inorder(n.left)+[n.val]+Probe.inorder(n.right) if n else []
    @staticmethod
    def max_path(root):
        best=-10**30
        def gain(n):
            nonlocal best
            if not n: return 0
            l=max(0,gain(n.left));r=max(0,gain(n.right));best=max(best,n.val+l+r);return n.val+max(l,r)
        gain(root);return best
    @staticmethod
    def serialize(n): return str(n.val)+' '+Probe.serialize(n.left)+Probe.serialize(n.right) if n else '# '
    @staticmethod
    def deserialize(s):
        tokens=iter(s.split())
        def read():
            token=next(tokens)
            return None if token=='#' else TreeNode(int(token),read(),read())
        return read()
    @staticmethod
    def clone(root):
        copies={}
        def copy(n):
            if n is None:return None
            if n in copies:return copies[n]
            c=Node(n.val);copies[n]=c;c.neighbors=[copy(v) for v in n.neighbors];return c
        return copy(root)
