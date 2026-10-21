function findMaximumSubarray(A) {
  let suffix = 0,
    best = 0;
  for (const value of A) {
    suffix = Math.max(0, suffix + value);
    best = Math.max(best, suffix);
  }
  return best;
}

module.exports = { findMaximumSubarray };
