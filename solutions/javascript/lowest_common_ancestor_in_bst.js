function lca(tree, s, b) {
  while (tree) {
    if (tree.data < s) tree = tree.right;
    else if (tree.data > b) tree = tree.left;
    else return tree.data;
  }
  throw new RangeError("Both targets must exist");
}

module.exports = { lca };
