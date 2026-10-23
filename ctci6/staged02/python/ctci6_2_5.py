class LinkedListNode:
    def __init__(self, value: int, next: 'LinkedListNode | None' = None):
        self.Value, self.Next = value, next
def AddLists(
    first: LinkedListNode | None, second: LinkedListNode | None, mostSignificantFirst: bool
) -> LinkedListNode | None:
    if mostSignificantFirst:
        left, right = [], []
        current = first
        while current is not None:
            left.append(current.Value)
            current = current.Next
        current = second
        while current is not None:
            right.append(current.Value)
            current = current.Next
        result, carry = None, 0
        while left or right or carry:
            total = carry + (left.pop() if left else 0) + (right.pop() if right else 0)
            result = LinkedListNode(total % 10, result)
            carry = total // 10
        return result
    dummy = LinkedListNode(0)
    tail = dummy
    p, q, carry = first, second, 0
    while p is not None or q is not None or carry:
        total = carry
        if p is not None:
            total += p.Value
            p = p.Next
        if q is not None:
            total += q.Value
            q = q.Next
        tail.Next = LinkedListNode(total % 10)
        tail = tail.Next
        carry = total // 10
    return dummy.Next
