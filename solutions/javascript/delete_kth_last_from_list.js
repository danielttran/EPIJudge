function removeKthLast(L, k) {
  const dummy = new ListNode(0, L);
  let fast = dummy,
    slow = dummy;
  for (let i = 0; i < k; i++) fast = fast.next;
  while (fast.next) {
    fast = fast.next;
    slow = slow.next;
  }
  slow.next = slow.next.next;
  return dummy.next;
}

module.exports = { removeKthLast };
