'use strict';
class LinkedListNode { constructor(value, next = null) { this.Value=value; this.Next=next; } }
function FindIntersection(first, second) {
  let p = first,
    q = second;
  while (p !== q) {
    p = p === null ? second : p.Next;
    q = q === null ? first : q.Next;
  }
  return p;
}
