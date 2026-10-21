function generateBalancedParentheses(num_pairs) {
  const result = [],
    buffer = Array(2 * num_pairs);
  function search(opened, closed) {
    const position = opened + closed;
    if (position === buffer.length) {
      result.push(buffer.join(""));
      return;
    }
    if (opened < num_pairs) {
      buffer[position] = "(";
      search(opened + 1, closed);
    }
    if (closed < opened) {
      buffer[position] = ")";
      search(opened, closed + 1);
    }
  }
  search(0, 0);
  return result;
}

module.exports = { generateBalancedParentheses };
