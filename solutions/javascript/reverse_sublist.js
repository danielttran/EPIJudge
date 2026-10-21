function reverseSublist(L, start, finish) {
  if (!L || finish <= start) return L;
  const dummy = new ListNode(0);
  dummy.next = L;
  let before = dummy;
  for (let i = 1; i < start; i++) before = before.next;
  const first = before.next;
  for (let i = start; i < finish; i++) {
    const moved = first.next;
    first.next = moved.next;
    moved.next = before.next;
    before.next = moved;
  }
  return dummy.next;
}

module.exports = { reverseSublist };
