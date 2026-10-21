function isSymmetric(tree) {
  function mirrors(a, b) {
    if (!a || !b) return !a && !b;
    return (
      a.data === b.data && mirrors(a.left, b.right) && mirrors(a.right, b.left)
    );
  }
  return !tree || mirrors(tree.left, tree.right);
}

module.exports = { isSymmetric };
