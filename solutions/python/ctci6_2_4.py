class LinkedListNode:
    def __init__(self, value: int, next: 'LinkedListNode | None' = None):
        self.Value, self.Next = value, next
def Partition(head: LinkedListNode | None, pivot: int) -> LinkedListNode | None:
    small_head = small_tail = large_head = large_tail = None
    current = head
    while current is not None:
        next_node = current.Next
        current.Next = None
        if current.Value < pivot:
            if small_tail is None:
                small_head = current
            else:
                small_tail.Next = current
            small_tail = current
        else:
            if large_tail is None:
                large_head = current
            else:
                large_tail.Next = current
            large_tail = current
        current = next_node
    if small_head is None:
        return large_head
    small_tail.Next = large_head
    return small_head
