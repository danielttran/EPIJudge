function rebuildBstFromPreorder(preorder_sequence) {
  if (!preorder_sequence.length) return null;
  const root = new BinaryTreeNode(preorder_sequence[0]),
    ancestors = [root];
  for (let i = 1; i < preorder_sequence.length; i++) {
    const value = preorder_sequence[i],
      node = new BinaryTreeNode(value);
    if (value < ancestors.at(-1).data) {
      ancestors.at(-1).left = node;
      node.parent = ancestors.at(-1);
    } else {
      let parent = null;
      while (ancestors.length && value >= ancestors.at(-1).data)
        parent = ancestors.pop();
      parent.right = node;
      node.parent = parent;
    }
    ancestors.push(node);
  }
  return root;
}

module.exports = { rebuildBstFromPreorder };
