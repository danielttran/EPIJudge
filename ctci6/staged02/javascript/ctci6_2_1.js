'use strict';
class LinkedListNode { constructor(value, next = null) { this.Value=value; this.Next=next; } }
function RemoveDups(head) {
  const seen = new Set();
  let previous = null,
    current = head;
  while (current !== null) {
    if (seen.has(current.Value)) previous.Next = current.Next;
    else {
      seen.add(current.Value);
      previous = current;
    }
    current = current.Next;
  }
}
