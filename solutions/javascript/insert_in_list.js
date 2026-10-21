function insertList(l, node_idx, new_node_data) {
  let selected = l;
  for (let position = 1; position < node_idx; position++)
    selected = selected.next;
  if (!selected) throw new RangeError("Selected node required");
  selected.next = new ListNode(new_node_data, selected.next);
  return l;
}

module.exports = { insertList };
