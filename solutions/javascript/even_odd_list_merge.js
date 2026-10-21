function evenOddMerge(L) {
  if (!L || !L.next) return L;
  let even = L,
    odd = L.next;
  const oddHead = odd;
  while (odd && odd.next) {
    even.next = odd.next;
    even = even.next;
    odd.next = even.next;
    odd = odd.next;
  }
  even.next = oddHead;
  return L;
}

module.exports = { evenOddMerge };
