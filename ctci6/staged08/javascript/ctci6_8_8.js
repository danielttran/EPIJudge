'use strict';
function PermutationsWithDuplicates(text) {
  const counts = Array(26).fill(0),
    buffer = Array(text.length),
    result = [];
  for (const char of text) ++counts[char.charCodeAt(0) - 97];
  function visit(depth) {
    if (depth === buffer.length) {
      result.push(buffer.join(""));
      return;
    }
    for (let letter = 0; letter < 26; ++letter) {
      if (counts[letter] > 0) {
        --counts[letter];
        buffer[depth] = String.fromCharCode(97 + letter);
        visit(depth + 1);
        ++counts[letter];
      }
    }
  }
  visit(0);
  return result;
}
