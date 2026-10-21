function findFirstMissingPositive(A) {
  for (let i = 0; i < A.length; i++)
    while (A[i] >= 1 && A[i] <= A.length && A[A[i] - 1] !== A[i]) {
      const destination = A[i] - 1;
      [A[i], A[destination]] = [A[destination], A[i]];
    }
  for (let i = 0; i < A.length; i++) if (A[i] !== i + 1) return i + 1;
  return A.length + 1;
}

module.exports = { findFirstMissingPositive };
