function findKLargestInBst(tree, k) {
  const result = [],
    pending = [];
  let current = tree;
  while (result.length < k && (current || pending.length)) {
    while (current) {
      pending.push(current);
      current = current.right;
    }
    current = pending.pop();
    result.push(current.data);
    current = current.left;
  }
  return result;
}

module.exports = { findKLargestInBst };
