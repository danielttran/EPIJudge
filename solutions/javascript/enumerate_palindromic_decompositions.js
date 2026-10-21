function palindromeDecompositions(text) {
  const n = text.length,
    palindrome = Array.from({ length: n }, () => Array(n).fill(false));
  for (let start = n - 1; start >= 0; start--)
    for (let end = start; end < n; end++)
      palindrome[start][end] =
        text[start] === text[end] &&
        (end - start < 2 || palindrome[start + 1][end - 1]);
  const result = [],
    parts = [];
  function search(start) {
    if (start === n) {
      result.push(parts.slice());
      return;
    }
    for (let end = start; end < n; end++)
      if (palindrome[start][end]) {
        parts.push(text.slice(start, end + 1));
        search(end + 1);
        parts.pop();
      }
  }
  search(0);
  return result;
}

module.exports = { palindromeDecompositions };
