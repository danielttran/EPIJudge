function copyPostingsList(head) {
  if (!head) return null;
  const copies = new Map([[head, new PostingListNode(head.order)]]),
    pending = [head];
  function copy(node) {
    if (!node) return null;
    if (!copies.has(node)) {
      copies.set(node, new PostingListNode(node.order));
      pending.push(node);
    }
    return copies.get(node);
  }
  for (let i = 0; i < pending.length; i++) {
    const node = pending[i],
      cloned = copies.get(node);
    cloned.next = copy(node.next);
    cloned.jump = copy(node.jump);
  }
  return copies.get(head);
}

module.exports = { copyPostingsList };
