def is_linked_list_a_palindrome(head):
    if head is None or head.next is None:
        return True
    middle = fast = head
    while fast.next is not None and fast.next.next is not None:
        middle, fast = middle.next, fast.next.next
    def reverse(node):
        previous = None
        while node is not None:
            following = node.next
            node.next = previous
            previous, node = node, following
        return previous
    second = reverse(middle.next)
    left, right, equal = head, second, True
    while right is not None:
        if left.data != right.data:
            equal = False
        left, right = left.next, right.next
    middle.next = reverse(second)
    return equal
