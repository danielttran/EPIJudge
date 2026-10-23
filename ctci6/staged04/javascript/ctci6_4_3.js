'use strict';
class TreeNode {constructor(data){this.Data=data;this.Left=this.Right=this.Parent=null;}}
class DepthLink {constructor(value){this.Value=value;this.Next=null;}}
function LinkedListsByDepth(root) {
  const heads = [];
  if (root === null) return heads;
  let current = [root];
  while (current.length) {
    let head = null,
      tail = null;
    const following = [];
    for (const node of current) {
      const link = new DepthLink(node);
      if (tail === null) head = link;
      else tail.Next = link;
      tail = link;
      if (node.Left !== null) following.push(node.Left);
      if (node.Right !== null) following.push(node.Right);
    }
    heads.push(head);
    current = following;
  }
  return heads;
}
