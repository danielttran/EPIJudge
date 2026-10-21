function findKthNodeBinaryTree(tree, k) {
  const pending = [];
  let current = tree;
  while (current || pending.length) {
    while (current) {
      pending.push(current);
      current = current.left;
    }
    current = pending.pop();
    if (--k === 0) return current.data;
    current = current.right;
  }
  throw new RangeError("Invalid rank");
}

module.exports = { findKthNodeBinaryTree };
