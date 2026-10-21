function postorderTraversal(tree) {
  const output = [];
  function visit(node) {
    if (!node) return;
    visit(node.left);
    visit(node.right);
    output.push(node.data);
  }
  visit(tree);
  return output;
}

module.exports = { postorderTraversal };
