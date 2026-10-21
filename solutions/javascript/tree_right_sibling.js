function constructRightSibling(tree) {
  if (!tree) return;
  tree.next = null;
  for (let level = tree; level.left; level = level.left)
    for (let node = level; node; node = node.next) {
      node.left.next = node.right;
      node.right.next = node.next ? node.next.left : null;
    }
}

module.exports = { constructRightSibling };
