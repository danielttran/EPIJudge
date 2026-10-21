function sumRootToLeaf(tree) {
  function visit(node, prefix) {
    if (!node) return 0;
    const value = prefix * 2 + node.data;
    return !node.left && !node.right
      ? value
      : visit(node.left, value) + visit(node.right, value);
  }
  return visit(tree, 0);
}

module.exports = { sumRootToLeaf };
