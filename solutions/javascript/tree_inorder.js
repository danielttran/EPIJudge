function inorderTraversal(tree) {
  const output = [];
  function visit(node) {
    if (!node) return;
    visit(node.left);
    output.push(node.data);
    visit(node.right);
  }
  visit(tree);
  return output;
}

module.exports = { inorderTraversal };
