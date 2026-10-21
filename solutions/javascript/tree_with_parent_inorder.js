function inorderTraversal(tree) {
  const output = [];
  let previous = null,
    current = tree;
  while (current) {
    let next;
    if (previous === current.parent) {
      if (current.left) next = current.left;
      else {
        output.push(current.data);
        next = current.right || current.parent;
      }
    } else if (previous === current.left) {
      output.push(current.data);
      next = current.right || current.parent;
    } else next = current.parent;
    previous = current;
    current = next;
  }
  return output;
}

module.exports = { inorderTraversal };
