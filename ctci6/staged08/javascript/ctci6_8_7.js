'use strict';
function PermutationsDistinct(text) {
  const chars = Array.from(text),
    result = [];
  function visit(depth) {
    if (depth === chars.length) {
      result.push(chars.join(""));
      return;
    }
    for (let i = depth; i < chars.length; ++i) {
      [chars[depth], chars[i]] = [chars[i], chars[depth]];
      visit(depth + 1);
      [chars[depth], chars[i]] = [chars[i], chars[depth]];
    }
  }
  visit(0);
  return result;
}
