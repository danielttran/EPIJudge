'use strict';
function MatchesPattern(pattern, text) {
  if (pattern.length === 0) return text.length === 0;
  let countA = 0;
  for (const symbol of pattern) if (symbol === "a") ++countA;
  const countB = pattern.length - countA,
    maximum = countA ? Math.floor(text.length / countA) : 0;
  for (let lengthA = 0; lengthA <= maximum; ++lengthA) {
    const remaining = text.length - countA * lengthA;
    if (countB === 0 ? remaining !== 0 : remaining % countB !== 0) continue;
    const lengthB = countB === 0 ? 0 : remaining / countB;
    let a = null,
      b = null,
      offset = 0,
      valid = true;
    for (const symbol of pattern) {
      const length = symbol === "a" ? lengthA : lengthB,
        part = text.slice(offset, offset + length);
      if (symbol === "a") {
        if (a === null) a = part;
        else if (a !== part) {
          valid = false;
          break;
        }
      } else {
        if (b === null) b = part;
        else if (b !== part) {
          valid = false;
          break;
        }
      }
      offset += length;
    }
    if (valid && offset === text.length) return true;
  }
  return false;
}

module.exports = {MatchesPattern};
