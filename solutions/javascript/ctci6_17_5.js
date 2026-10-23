'use strict';
function LongestLettersDigits(text) {
  const n = text.length,
    first = Array(2 * n + 1).fill(-2);
  first[n] = -1;
  let balance = 0,
    best = 0,
    start = -1,
    end = -1;
  for (let i = 0; i < n; ++i) {
    balance += text[i] >= "0" && text[i] <= "9" ? -1 : 1;
    const slot = balance + n;
    if (first[slot] === -2) first[slot] = i;
    else if (i - first[slot] > best) {
      best = i - first[slot];
      start = first[slot] + 1;
      end = i;
    }
  }
  return [start, end];
}

module.exports = {LongestLettersDigits};
