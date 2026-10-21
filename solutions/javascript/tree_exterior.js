function createOutputList(tree) {
  const output = [];
  if (!tree) return output;
  const leaf = (node) => !node.left && !node.right;
  output.push(tree.data);
  for (let node = tree.left; node; node = node.left || node.right)
    if (!leaf(node)) output.push(node.data);
  function leaves(node) {
    if (!node) return;
    if (leaf(node)) output.push(node.data);
    else {
      leaves(node.left);
      leaves(node.right);
    }
  }
  leaves(tree.left);
  leaves(tree.right);
  const right = [];
  for (let node = tree.right; node; node = node.right || node.left)
    if (!leaf(node)) right.push(node.data);
  for (let i = right.length - 1; i >= 0; i--) output.push(right[i]);
  return output;
}

module.exports = { createOutputList };
