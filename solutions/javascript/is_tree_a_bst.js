function isBinaryTreeBst(tree) {
  const pending = tree ? [[tree, -Infinity, Infinity]] : [];
  while (pending.length) {
    const [node, low, high] = pending.pop();
    if (node.data < low || node.data > high) return false;
    if (node.left) pending.push([node.left, low, node.data]);
    if (node.right) pending.push([node.right, node.data, high]);
  }
  return true;
}

module.exports = { isBinaryTreeBst };
