'use strict';
function RecursiveMultiply(first, second) {
  const smaller = Math.min(first, second),
    larger = Math.max(first, second);
  if (smaller === 0) return 0;
  const half = RecursiveMultiply(smaller >>> 1, larger);
  return half + half + ((smaller & 1) !== 0 ? larger : 0);
}

module.exports = {RecursiveMultiply};
