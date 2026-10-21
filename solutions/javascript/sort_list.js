function stableSortList(L) {
  if (!L || !L.next) return L;
  let slow = L,
    fast = L.next;
  while (fast && fast.next) {
    slow = slow.next;
    fast = fast.next.next;
  }
  const right = slow.next;
  slow.next = null;
  let first = stableSortList(L),
    second = stableSortList(right);
  const dummy = new ListNode(0);
  let tail = dummy;
  while (first && second) {
    if (first.data <= second.data) {
      tail.next = first;
      first = first.next;
    } else {
      tail.next = second;
      second = second.next;
    }
    tail = tail.next;
  }
  tail.next = first || second;
  return dummy.next;
}

module.exports = { stableSortList };
