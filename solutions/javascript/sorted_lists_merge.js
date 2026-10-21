function mergeTwoSortedLists(L1, L2) {
  const dummy = new ListNode(0);
  let tail = dummy;
  while (L1 && L2) {
    if (L1.data <= L2.data) {
      tail.next = L1;
      L1 = L1.next;
    } else {
      tail.next = L2;
      L2 = L2.next;
    }
    tail = tail.next;
  }
  tail.next = L1 || L2;
  return dummy.next;
}

module.exports = { mergeTwoSortedLists };
