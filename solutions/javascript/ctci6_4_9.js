'use strict';
class TreeNode {constructor(data){this.Data=data;this.Left=this.Right=this.Parent=null;}}
function BstInsertionSequences(root) {
  const result = [],
    path = [];
  function visit(available) {
    if (available.length === 0) {
      result.push(path.slice());
      return;
    }
    for (let i = 0; i < available.length; ++i) {
      const node = available[i],
        following = available.slice(0, i).concat(available.slice(i + 1));
      if (node.Left !== null) following.push(node.Left);
      if (node.Right !== null) following.push(node.Right);
      path.push(node.Data);
      visit(following);
      path.pop();
    }
  }
  visit(root === null ? [] : [root]);
  return result;
}

module.exports = {TreeNode,BstInsertionSequences};
