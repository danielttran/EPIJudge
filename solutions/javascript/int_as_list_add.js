function addTwoNumbers(L1, L2) {
  const dummy = new ListNode(0);
  let tail = dummy,
    carry = 0;
  while (L1 || L2 || carry) {
    const sum = (L1 ? L1.data : 0) + (L2 ? L2.data : 0) + carry;
    tail.next = new ListNode(sum % 10);
    tail = tail.next;
    carry = Math.floor(sum / 10);
    L1 = L1 ? L1.next : null;
    L2 = L2 ? L2.next : null;
  }
  return dummy.next;
}

module.exports = { addTwoNumbers };
