'use strict';
class TreeNode {constructor(data){this.Data=data;this.Left=this.Right=this.Parent=null;}}
function ContainsExactSubtree(large, small) {
  if (small === null) return true;
  function encode(root) {
    const tokens = [],
      stack = [root];
    while (stack.length) {
      const node = stack.pop();
      if (node === null) tokens.push("#");
      else {
        tokens.push("V" + String(node.Data));
        stack.push(node.Right, node.Left);
      }
    }
    return tokens;
  }
  const text = encode(large),
    pattern = encode(small),
    prefix = new Array(pattern.length).fill(0);
  for (let i = 1; i < pattern.length; ++i) {
    let matched = prefix[i - 1];
    while (matched > 0 && pattern[i] !== pattern[matched]) matched = prefix[matched - 1];
    if (pattern[i] === pattern[matched]) ++matched;
    prefix[i] = matched;
  }
  let matched = 0;
  for (const token of text) {
    while (matched > 0 && token !== pattern[matched]) matched = prefix[matched - 1];
    if (token === pattern[matched]) ++matched;
    if (matched === pattern.length) return true;
  }
  return false;
}
