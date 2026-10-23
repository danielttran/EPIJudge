'use strict';
class LinkedListNode { constructor(value, next = null) { this.Value=value; this.Next=next; } }
function KthToLast(head, k) {
  if (k <= 0) return null;
  let lead = head;
  for (let i = 0; i < k; ++i) {
    if (lead === null) return null;
    lead = lead.Next;
  }
  let follow = head;
  while (lead !== null) {
    lead = lead.Next;
    follow = follow.Next;
  }
  return follow;
}

module.exports = {LinkedListNode,KthToLast};
