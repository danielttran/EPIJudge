function deletionFromList(head, node_to_delete_idx) {
  let node = head;
  for (let i = 0; i < node_to_delete_idx; i++) node = node.next;
  node.data = node.next.data;
  node.next = node.next.next;
  return head;
}

module.exports = { deletionFromList };
