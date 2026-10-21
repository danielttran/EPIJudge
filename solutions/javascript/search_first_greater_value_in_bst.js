function findFirstGreaterThanK(tree, k) {
  let candidate = -1;
  while (tree) {
    if (tree.data > k) {
      candidate = tree.data;
      tree = tree.left;
    } else tree = tree.right;
  }
  return candidate;
}

module.exports = { findFirstGreaterThanK };
