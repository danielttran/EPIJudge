'use strict';
class TreeNode {constructor(data){this.Data=data;this.Left=this.Right=this.Parent=null;}}
function InorderSuccessor(node) {
  if (node === null) return null;
  if (node.Right !== null) {
    let following = node.Right;
    while (following.Left !== null) following = following.Left;
    return following;
  }
  let current = node,
    parent = node.Parent;
  while (parent !== null && current === parent.Right) {
    current = parent;
    parent = parent.Parent;
  }
  return parent;
}
