function searchBst(tree, key) {
  while (tree) {
    if (tree.data === key) return key;
    tree = key < tree.data ? tree.left : tree.right;
  }
  return -1;
}

module.exports = { searchBst };
