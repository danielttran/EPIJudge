class LinkedListNode:
    def __init__(self, value: int, next: 'LinkedListNode | None' = None):
        self.Value, self.Next = value, next
def FindLoopEntry(head: LinkedListNode | None) -> LinkedListNode | None:
    slow = fast = head
    while fast is not None and fast.Next is not None:
        slow, fast = slow.Next, fast.Next.Next
        if slow is fast:
            break
    if fast is None or fast.Next is None:
        return None
    slow = head
    while slow is not fast:
        slow, fast = slow.Next, fast.Next
    return slow
