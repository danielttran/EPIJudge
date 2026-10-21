function bstToDoublyLinkedList(tree) {
  const stack = [];
  let head = null,
    previous = null,
    current = tree;
  while (current || stack.length) {
    while (current) {
      stack.push(current);
      current = current.left;
    }
    current = stack.pop();
    const right = current.right;
    current.left = previous;
    if (!previous) head = current;
    else previous.right = current;
    previous = current;
    current = right;
  }
  if (previous) previous.right = null;
  return head;
}

module.exports = { bstToDoublyLinkedList };
