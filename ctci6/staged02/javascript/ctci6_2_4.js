'use strict';
class LinkedListNode { constructor(value, next = null) { this.Value=value; this.Next=next; } }
function Partition(head, pivot) {
  let smallHead = null,
    smallTail = null,
    largeHead = null,
    largeTail = null;
  let current = head;
  while (current !== null) {
    const next = current.Next;
    current.Next = null;
    if (current.Value < pivot) {
      if (smallTail === null) smallHead = current;
      else smallTail.Next = current;
      smallTail = current;
    } else {
      if (largeTail === null) largeHead = current;
      else largeTail.Next = current;
      largeTail = current;
    }
    current = next;
  }
  if (smallHead === null) return largeHead;
  smallTail.Next = largeHead;
  return smallHead;
}
