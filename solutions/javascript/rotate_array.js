function rotateArray(A, rotate_amount) {
  if (!A.length) return A;
  const amount = ((rotate_amount % A.length) + A.length) % A.length;
  function reverse(l, r) {
    while (l < r) {
      [A[l], A[r]] = [A[r], A[l]];
      l++;
      r--;
    }
  }
  reverse(0, A.length - 1);
  reverse(0, amount - 1);
  reverse(amount, A.length - 1);
  return A;
}

module.exports = { rotateArray };
