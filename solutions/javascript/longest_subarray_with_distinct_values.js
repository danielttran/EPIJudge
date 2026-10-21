function longestSubarrayWithDistinctEntries(A) {
  const last = new Map();
  let left = 0,
    best = 0;
  for (let right = 0; right < A.length; right++) {
    if (last.has(A[right])) left = Math.max(left, last.get(A[right]) + 1);
    last.set(A[right], right);
    best = Math.max(best, right - left + 1);
  }
  return best;
}

module.exports = { longestSubarrayWithDistinctEntries };
