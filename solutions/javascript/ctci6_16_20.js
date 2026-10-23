'use strict';
function T9Words(digits, dictionary) {
  const mapping = "22233344455566677778889999",
    result = [];
  for (const word of dictionary) {
    if (word.length !== digits.length) continue;
    let valid = true;
    for (let i = 0; i < word.length; ++i)
      if (mapping[word.charCodeAt(i) - 97] !== digits[i]) {
        valid = false;
        break;
      }
    if (valid) result.push(word);
  }
  return result;
}

module.exports = {T9Words};
