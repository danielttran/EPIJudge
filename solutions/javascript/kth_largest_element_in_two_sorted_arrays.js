function findKthInTwoSortedArrays(A, B, k) {
  let a = 0,
    b = 0;
  for (;;) {
    if (a === A.length) return B[b + k - 1];
    if (b === B.length) return A[a + k - 1];
    if (k === 1) return Math.min(A[a], B[b]);
    const takeA = Math.min(Math.floor(k / 2), A.length - a),
      takeB = Math.min(Math.floor(k / 2), B.length - b);
    if (A[a + takeA - 1] <= B[b + takeB - 1]) {
      a += takeA;
      k -= takeA;
    } else {
      b += takeB;
      k -= takeB;
    }
  }
}

module.exports = { findKthInTwoSortedArrays };
