class LinkedListNode:
    def __init__(self, value: int, next: 'LinkedListNode | None' = None):
        self.Value, self.Next = value, next
def KthToLast(head: LinkedListNode | None, k: int) -> LinkedListNode | None:
    if k <= 0:
        return None
    lead = head
    for _ in range(k):
        if lead is None:
            return None
        lead = lead.Next
    follow = head
    while lead is not None:
        lead, follow = lead.Next, follow.Next
    return follow
