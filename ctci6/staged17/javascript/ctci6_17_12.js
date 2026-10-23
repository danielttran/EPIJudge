'use strict';
class BiNode {constructor(data){this.Data=data;this.Node1=null;this.Node2=null;}}
function ConvertBiNode(root) {
  const stack = [];
  let current = root,
    previous = null,
    head = null;
  while (current !== null || stack.length) {
    while (current !== null) {
      stack.push(current);
      current = current.Node1;
    }
    const node = stack.pop(),
      right = node.Node2;
    node.Node1 = previous;
    if (previous === null) head = node;
    else previous.Node2 = node;
    previous = node;
    current = right;
  }
  if (previous !== null) previous.Node2 = null;
  return head;
}
