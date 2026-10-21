function listPivoting(head, x) {
  const heads = [new ListNode(0), new ListNode(0), new ListNode(0)],
    tails = heads.slice();
  while (head) {
    const next = head.next;
    head.next = null;
    const group = head.data < x ? 0 : head.data === x ? 1 : 2;
    tails[group].next = head;
    tails[group] = head;
    head = next;
  }
  tails[1].next = heads[2].next;
  tails[0].next = heads[1].next;
  return heads[0].next;
}

module.exports = { listPivoting };
