function rangeLookupInBst(tree, i) {
  const result = [];
  function visit(node) {
    if (!node) return;
    if (node.data >= i[0]) visit(node.left);
    if (node.data >= i[0] && node.data <= i[1]) result.push(node.data);
    if (node.data <= i[1]) visit(node.right);
  }
  visit(tree);
  return result;
}

module.exports = { rangeLookupInBst };
