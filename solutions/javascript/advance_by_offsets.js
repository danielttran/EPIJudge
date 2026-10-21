function canReachEnd(A) {
  let farthest = 0;
  for (let i = 0; i < A.length && i <= farthest; i++) {
    farthest = Math.max(farthest, i + A[i]);
    if (farthest >= A.length - 1) return true;
  }
  return !A.length;
}

module.exports = { canReachEnd };
