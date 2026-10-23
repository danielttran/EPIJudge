class LinkedListNode:
    def __init__(self, value: int, next: 'LinkedListNode | None' = None):
        self.Value, self.Next = value, next
def DeleteMiddle(target: LinkedListNode | None) -> bool:
    if target is None or target.Next is None:
        return False
    successor = target.Next
    target.Value, target.Next = successor.Value, successor.Next
    return True
