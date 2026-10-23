'use strict';
class TreeNode {constructor(data){this.Data=data;this.Left=this.Right=this.Parent=null;}}
function IsHeightBalanced(root) {
  if (root === null) return true;
  const heights = new Map(),
    stack = [[root, false]];
  while (stack.length) {
    const [node, exiting] = stack.pop();
    if (!exiting) {
      stack.push([node, true]);
      if (node.Right !== null) stack.push([node.Right, false]);
      if (node.Left !== null) stack.push([node.Left, false]);
    } else {
      const left = heights.get(node.Left) || 0,
        right = heights.get(node.Right) || 0;
      if (Math.abs(left - right) > 1) return false;
      heights.set(node, 1 + Math.max(left, right));
    }
  }
  return true;
}

module.exports = {TreeNode,IsHeightBalanced};
