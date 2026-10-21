function zippingLinkedList(L) {
  if (!L || !L.next) return L;
  let slow = L,
    fast = L;
  while (fast.next && fast.next.next) {
    slow = slow.next;
    fast = fast.next.next;
  }
  let second = slow.next;
  slow.next = null;
  let reversed = null;
  while (second) {
    const next = second.next;
    second.next = reversed;
    reversed = second;
    second = next;
  }
  let first = L;
  while (reversed) {
    const nextFirst = first.next,
      nextSecond = reversed.next;
    first.next = reversed;
    reversed.next = nextFirst;
    first = nextFirst;
    reversed = nextSecond;
  }
  return L;
}

module.exports = { zippingLinkedList };
