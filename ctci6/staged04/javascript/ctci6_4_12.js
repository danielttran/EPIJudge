'use strict';
class TreeNode {constructor(data){this.Data=data;this.Left=this.Right=this.Parent=null;}}
function CountDownwardSumPaths(root, target) {
  if (root === null) return 0;
  const prefix = new Map([[0, 1]]),
    stack = [[root, 0, false]];
  let answer = 0;
  while (stack.length) {
    let [node, running, exiting] = stack.pop();
    if (exiting) {
      const count = prefix.get(running) - 1;
      if (count === 0) prefix.delete(running);
      else prefix.set(running, count);
      continue;
    }
    running += node.Data;
    answer += prefix.get(running - target) || 0;
    prefix.set(running, (prefix.get(running) || 0) + 1);
    stack.push([node, running, true]);
    if (node.Right !== null) stack.push([node.Right, running, false]);
    if (node.Left !== null) stack.push([node.Left, running, false]);
  }
  return answer;
}
