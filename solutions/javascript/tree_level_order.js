function binaryTreeDepthOrder(tree) {
  const output = [];
  let level = tree ? [tree] : [];
  while (level.length) {
    const values = [],
      next = [];
    for (const node of level) {
      values.push(node.data);
      if (node.left) next.push(node.left);
      if (node.right) next.push(node.right);
    }
    output.push(values);
    level = next;
  }
  return output;
}

module.exports = { binaryTreeDepthOrder };
