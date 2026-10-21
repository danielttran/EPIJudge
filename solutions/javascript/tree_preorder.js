function preorderTraversal(tree) {
  const output = [];
  function visit(node) {
    if (!node) return;
    output.push(node.data);
    visit(node.left);
    visit(node.right);
  }
  visit(tree);
  return output;
}

module.exports = { preorderTraversal };
