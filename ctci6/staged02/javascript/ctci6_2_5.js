'use strict';
class LinkedListNode { constructor(value, next = null) { this.Value=value; this.Next=next; } }
function AddLists(first, second, mostSignificantFirst) {
  if (mostSignificantFirst) {
    const left = [],
      right = [];
    for (let p = first; p !== null; p = p.Next) left.push(p.Value);
    for (let p = second; p !== null; p = p.Next) right.push(p.Value);
    let result = null,
      carry = 0;
    while (left.length || right.length || carry) {
      const total = carry + (left.length ? left.pop() : 0) + (right.length ? right.pop() : 0);
      result = new LinkedListNode(total % 10, result);
      carry = Math.floor(total / 10);
    }
    return result;
  }
  const dummy = new LinkedListNode(0);
  let tail = dummy,
    p = first,
    q = second,
    carry = 0;
  while (p !== null || q !== null || carry) {
    let total = carry;
    if (p !== null) {
      total += p.Value;
      p = p.Next;
    }
    if (q !== null) {
      total += q.Value;
      q = q.Next;
    }
    tail.Next = new LinkedListNode(total % 10);
    tail = tail.Next;
    carry = Math.floor(total / 10);
  }
  return dummy.Next;
}
