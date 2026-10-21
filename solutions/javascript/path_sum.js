function hasPathSum(tree, remaining_weight) {
  function visit(node, remaining) {
    if (!node) return false;
    remaining -= BigInt(node.data);
    if (!node.left && !node.right) return remaining === 0n;
    return visit(node.left, remaining) || visit(node.right, remaining);
  }
  return visit(tree, BigInt(remaining_weight));
}

module.exports = { hasPathSum };
