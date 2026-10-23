class LinkedListNode:
    def __init__(self, value: int, next: 'LinkedListNode | None' = None):
        self.Value, self.Next = value, next
def FindIntersection(
    first: LinkedListNode | None, second: LinkedListNode | None
) -> LinkedListNode | None:
    p, q = first, second
    while p is not q:
        p = second if p is None else p.Next
        q = first if q is None else q.Next
    return p
