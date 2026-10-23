class LinkedListNode:
    def __init__(self, value: int, next: 'LinkedListNode | None' = None):
        self.Value, self.Next = value, next
def IsPalindrome(head: LinkedListNode | None) -> bool:
    values = []
    current = head
    while current is not None:
        values.append(current.Value)
        current = current.Next
    for i in range(len(values) // 2):
        if values[i] != values[len(values) - 1 - i]:
            return False
    return True
