'use strict';
function SmallestDifference(first, second) {
  if (!first.length || !second.length) return -1;
  const a = first.slice().sort((x, y) => x - y),
    b = second.slice().sort((x, y) => x - y);
  let i = 0,
    j = 0,
    best = 4294967295;
  while (i < a.length && j < b.length) {
    const difference = a[i] - b[j];
    best = Math.min(best, Math.abs(difference));
    if (difference === 0) return 0;
    if (difference < 0) ++i;
    else ++j;
  }
  return best;
}

module.exports = {SmallestDifference};
