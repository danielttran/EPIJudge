function findSuccessor(tree, node_idx) {
  const stack = tree ? [tree] : [];
  let node = null;
  while (stack.length) {
    const current = stack.pop();
    if (current.data === node_idx) {
      node = current;
      break;
    }
    if (current.right) stack.push(current.right);
    if (current.left) stack.push(current.left);
  }
  if (!node) return -1;
  if (node.right) {
    node = node.right;
    while (node.left) node = node.left;
    return node.data;
  }
  while (node.parent && node.parent.right === node) node = node.parent;
  return node.parent ? node.parent.data : -1;
}

module.exports = { findSuccessor };
