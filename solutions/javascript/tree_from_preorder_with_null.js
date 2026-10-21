function reconstructPreorder(data) {
  let position = 0;
  function build() {
    if (position >= data.length) return null;
    const token = data[position++];
    if (token === "null" || token === null) return null;
    const root = new BinaryTreeNode(Number(token));
    root.left = build();
    root.right = build();
    if (root.left) root.left.parent = root;
    if (root.right) root.right.parent = root;
    root.size =
      1 + (root.left ? root.left.size : 0) + (root.right ? root.right.size : 0);
    return root;
  }
  return build();
}

module.exports = { reconstructPreorder };
