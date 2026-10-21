function binaryTreeFromPreorderInorder(preorder, inorder) {
  const positions = new Map(inorder.map((value, index) => [value, index]));
  let next = 0;
  function build(left, right) {
    if (left >= right) return null;
    const value = preorder[next++],
      middle = positions.get(value),
      root = new BinaryTreeNode(value);
    root.left = build(left, middle);
    root.right = build(middle + 1, right);
    if (root.left) root.left.parent = root;
    if (root.right) root.right.parent = root;
    root.size = right - left;
    return root;
  }
  return build(0, inorder.length);
}

module.exports = { binaryTreeFromPreorderInorder };
