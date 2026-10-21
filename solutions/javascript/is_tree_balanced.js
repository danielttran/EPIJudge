function isBalancedBinaryTree(tree) {
  function height(node) {
    if (!node) return 0;
    const left = height(node.left);
    if (left < 0) return -1;
    const right = height(node.right);
    if (right < 0 || Math.abs(left - right) > 1) return -1;
    return Math.max(left, right) + 1;
  }
  return height(tree) >= 0;
}

module.exports = { isBalancedBinaryTree };
