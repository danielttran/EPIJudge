function buildMinHeightBstFromSortedArray(values) {
  function build(start, end, parent = null) {
    if (start >= end) return null;
    const middle = start + Math.floor((end - start) / 2),
      node = new BinaryTreeNode(values[middle]);
    node.parent = parent;
    node.left = build(start, middle, node);
    node.right = build(middle + 1, end, node);
    node.size = end - start;
    return node;
  }
  return build(0, values.length);
}

module.exports = { buildMinHeightBstFromSortedArray };
