from list_node import ListNode

def stable_sort_list(head):
    if head is None or head.next is None:
        return head
    slow, fast = head, head.next
    while fast is not None and fast.next is not None:
        slow, fast = slow.next, fast.next.next
    second = slow.next
    slow.next = None
    first, second = stable_sort_list(head), stable_sort_list(second)
    dummy = tail = ListNode(0)
    while first is not None and second is not None:
        if first.data <= second.data:
            tail.next, first = first, first.next
        else:
            tail.next, second = second, second.next
        tail = tail.next
    tail.next = first if first is not None else second
    return dummy.next
