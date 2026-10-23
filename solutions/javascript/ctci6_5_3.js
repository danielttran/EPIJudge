'use strict';
function LongestOnesAfterFlip(word) {
  const bits = word >>> 0;
  let left = 0,
    zeros = 0,
    best = 0;
  for (let right = 0; right < 32; ++right) {
    if (((bits >>> right) & 1) === 0) ++zeros;
    while (zeros > 1) {
      if (((bits >>> left) & 1) === 0) --zeros;
      ++left;
    }
    best = Math.max(best, right - left + 1);
  }
  return best;
}

module.exports = {LongestOnesAfterFlip};
