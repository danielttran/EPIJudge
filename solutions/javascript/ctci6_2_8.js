'use strict';
class LinkedListNode { constructor(value, next = null) { this.Value=value; this.Next=next; } }
function FindLoopEntry(head) {
  let slow = head,
    fast = head;
  while (fast !== null && fast.Next !== null) {
    slow = slow.Next;
    fast = fast.Next.Next;
    if (slow === fast) break;
  }
  if (fast === null || fast.Next === null) return null;
  slow = head;
  while (slow !== fast) {
    slow = slow.Next;
    fast = fast.Next;
  }
  return slow;
}

module.exports = {LinkedListNode,FindLoopEntry};
