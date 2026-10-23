'use strict';
function ShortestCoveringRange(big, small) {
  if (small.length === 0) return [-1, -1];
  const counts = new Map(small.map((v) => [v, 0]));
  let missing = small.length,
    left = 0,
    start = -1,
    end = -1;
  for (let right = 0; right < big.length; ++right) {
    const value = big[right];
    if (counts.has(value)) {
      if (counts.get(value) === 0) --missing;
      counts.set(value, counts.get(value) + 1);
    }
    while (missing === 0) {
      if (start === -1 || right - left < end - start) {
        start = left;
        end = right;
      }
      const removed = big[left];
      if (counts.has(removed)) {
        counts.set(removed, counts.get(removed) - 1);
        if (counts.get(removed) === 0) ++missing;
      }
      ++left;
    }
  }
  return [start, end];
}
