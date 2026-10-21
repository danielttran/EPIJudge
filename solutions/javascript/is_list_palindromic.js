function isLinkedListAPalindrome(L) {
  if (!L || !L.next) return true;
  let middle = L,
    fast = L;
  while (fast.next && fast.next.next) {
    middle = middle.next;
    fast = fast.next.next;
  }
  function reverse(node) {
    let previous = null;
    while (node) {
      const next = node.next;
      node.next = previous;
      previous = node;
      node = next;
    }
    return previous;
  }
  const second = reverse(middle.next);
  let equal = true,
    left = L;
  for (let right = second; right; right = right.next) {
    if (left.data !== right.data) equal = false;
    left = left.next;
  }
  middle.next = reverse(second);
  return equal;
}

module.exports = { isLinkedListAPalindrome };
