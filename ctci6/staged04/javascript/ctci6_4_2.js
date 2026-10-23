'use strict';
class TreeNode {constructor(data){this.Data=data;this.Left=this.Right=this.Parent=null;}}
function CreateMinimalBst(sortedValues) {
  function build(lower, upper, parent) {
    if (lower >= upper) return null;
    const middle = lower + Math.floor((upper - lower) / 2),
      node = new TreeNode(sortedValues[middle]);
    node.Parent = parent;
    node.Left = build(lower, middle, node);
    node.Right = build(middle + 1, upper, node);
    return node;
  }
  return build(0, sortedValues.length, null);
}
