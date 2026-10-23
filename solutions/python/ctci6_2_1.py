class LinkedListNode:
    def __init__(self, value: int, next: 'LinkedListNode | None' = None):
        self.Value, self.Next = value, next
def RemoveDups(head: LinkedListNode | None) -> None:
    seen = set()
    previous, current = None, head
    while current is not None:
        if current.Value in seen:
            previous.Next = current.Next
        else:
            seen.add(current.Value)
            previous = current
        current = current.Next
