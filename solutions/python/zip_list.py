def zipping_linked_list(head):
    if head is None or head.next is None:
        return head
    slow = fast = head
    while fast.next is not None and fast.next.next is not None:
        slow, fast = slow.next, fast.next.next
    second = slow.next
    slow.next = None
    previous = None
    while second is not None:
        following = second.next
        second.next = previous
        previous, second = second, following
    first, second = head, previous
    while second is not None:
        next_first, next_second = first.next, second.next
        first.next = second
        second.next = next_first
        first, second = next_first, next_second
    return head
