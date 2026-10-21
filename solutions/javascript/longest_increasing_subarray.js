function findLongestIncreasingSubarray(A) {
  let best = 0,
    length = 0;
  for (let i = 0; i < A.length; i++) {
    length = i > 0 && A[i] > A[i - 1] ? length + 1 : 1;
    best = Math.max(best, length);
  }
  return best;
}

module.exports = { findLongestIncreasingSubarray };
