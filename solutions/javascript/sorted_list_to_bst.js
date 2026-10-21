function buildBstFromSortedDoublyList(head, count) {
  let cursor = head;
  function build(size) {
    if (!size) return null;
    const left = build(Math.floor(size / 2)),
      root = cursor;
    cursor = cursor.right;
    root.left = left;
    root.right = build(size - Math.floor(size / 2) - 1);
    root.parent = null;
    if (root.left) root.left.parent = root;
    if (root.right) root.right.parent = root;
    root.size = size;
    return root;
  }
  return build(count);
}

module.exports = { buildBstFromSortedDoublyList };
