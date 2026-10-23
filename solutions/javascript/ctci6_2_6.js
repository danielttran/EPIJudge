'use strict';
class LinkedListNode { constructor(value, next = null) { this.Value=value; this.Next=next; } }
function IsPalindrome(head) {
  const values = [];
  for (let p = head; p !== null; p = p.Next) values.push(p.Value);
  for (let i = 0; i < Math.floor(values.length / 2); ++i) {
    if (values[i] !== values[values.length - 1 - i]) return false;
  }
  return true;
}

module.exports = {LinkedListNode,IsPalindrome};
