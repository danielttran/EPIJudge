'use strict';
class LinkedListNode { constructor(value, next = null) { this.Value=value; this.Next=next; } }
function DeleteMiddle(target) {
  if (target === null || target.Next === null) return false;
  const successor = target.Next;
  target.Value = successor.Value;
  target.Next = successor.Next;
  return true;
}

module.exports = {LinkedListNode,DeleteMiddle};
