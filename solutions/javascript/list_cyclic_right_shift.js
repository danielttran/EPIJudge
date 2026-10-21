function cyclicallyRightShiftList(L, k) {
  if (!L) return null;
  let length = 1,
    tail = L;
  while (tail.next) {
    tail = tail.next;
    length++;
  }
  k = ((k % length) + length) % length;
  if (!k) return L;
  let newTail = L;
  for (let i = 1; i < length - k; i++) newTail = newTail.next;
  const newHead = newTail.next;
  tail.next = L;
  newTail.next = null;
  return newHead;
}

module.exports = { cyclicallyRightShiftList };
