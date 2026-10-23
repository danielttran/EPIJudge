'use strict';
class TreeNode {constructor(data){this.Data=data;this.Left=this.Right=this.Parent=null;}}
function IsDuplicateLeftBst(root) {
  const stack = root === null ? [] : [[root, -2147483649, 2147483647]];
  while (stack.length) {
    const [node, lower, upper] = stack.pop();
    if (node.Data <= lower || node.Data > upper) return false;
    if (node.Right !== null) stack.push([node.Right, node.Data, upper]);
    if (node.Left !== null) stack.push([node.Left, lower, node.Data]);
  }
  return true;
}
