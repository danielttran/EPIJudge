function createListOfLeaves(tree) {
  const result = [];
  function visit(node) {
    if (!node) return;
    if (!node.left && !node.right) {
      result.push(node.data);
      return;
    }
    visit(node.left);
    visit(node.right);
  }
  visit(tree);
  return result;
}

module.exports = { createListOfLeaves };
