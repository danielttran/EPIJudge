function mergeTwoBsts(A, B) {
  function inorder(node) {
    const values = [],
      stack = [];
    while (node || stack.length) {
      while (node) {
        stack.push(node);
        node = node.left;
      }
      node = stack.pop();
      values.push(node.data);
      node = node.right;
    }
    return values;
  }
  const first = inorder(A),
    second = inorder(B),
    merged = [];
  let i = 0,
    j = 0;
  while (i < first.length || j < second.length)
    merged.push(
      j === second.length || (i < first.length && first[i] <= second[j])
        ? first[i++]
        : second[j++],
    );
  function build(start, end, parent = null) {
    if (start >= end) return null;
    const middle = start + Math.floor((end - start) / 2),
      node = new BinaryTreeNode(merged[middle]);
    node.parent = parent;
    node.left = build(start, middle, node);
    node.right = build(middle + 1, end, node);
    node.size = end - start;
    return node;
  }
  return build(0, merged.length);
}

module.exports = { mergeTwoBsts };
