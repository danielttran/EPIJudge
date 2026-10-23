'use strict';
class TreeNode {constructor(data){this.Data=data;this.Left=this.Right=this.Parent=null;}}
function FirstCommonAncestor(first, second) {
  if (first === null || second === null) return null;
  let depthFirst = 0,
    depthSecond = 0;
  for (let cursor = first; cursor !== null; cursor = cursor.Parent) ++depthFirst;
  for (let cursor = second; cursor !== null; cursor = cursor.Parent) ++depthSecond;
  while (depthFirst > depthSecond) {
    first = first.Parent;
    --depthFirst;
  }
  while (depthSecond > depthFirst) {
    second = second.Parent;
    --depthSecond;
  }
  while (first !== second) {
    first = first.Parent;
    second = second.Parent;
  }
  return first;
}
