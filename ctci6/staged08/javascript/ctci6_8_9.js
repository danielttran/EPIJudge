'use strict';
function GenerateParentheses(pairs) {
  const buffer = Array(2 * pairs),
    result = [];
  function visit(opened, closed) {
    const position = opened + closed;
    if (position === buffer.length) {
      result.push(buffer.join(""));
      return;
    }
    if (opened < pairs) {
      buffer[position] = "(";
      visit(opened + 1, closed);
    }
    if (closed < opened) {
      buffer[position] = ")";
      visit(opened, closed + 1);
    }
  }
  visit(0, 0);
  return result;
}
