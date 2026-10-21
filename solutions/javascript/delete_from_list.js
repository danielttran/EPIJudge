function deleteFromList(head, node_idx) {
  let previous = head;
  for (let i = 1; i < node_idx; i++) previous = previous.next;
  previous.next = previous.next.next;
  return head;
}

module.exports = { deleteFromList };
