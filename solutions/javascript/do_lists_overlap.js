function overlappingLists(first, second) {
  const firstNodes = new Set();
  while (first && !firstNodes.has(first)) {
    firstNodes.add(first);
    first = first.next;
  }
  const visited = new Set();
  while (second && !visited.has(second)) {
    visited.add(second);
    if (firstNodes.has(second)) return second;
    second = second.next;
  }
  return null;
}

module.exports = { overlappingLists };
