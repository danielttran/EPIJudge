function matrixSearch(A, x) {
  if (!A.length || !A[0].length) return false;
  let row = 0,
    column = A[0].length - 1;
  while (row < A.length && column >= 0) {
    const value = A[row][column];
    if (value === x) return true;
    if (value > x) column--;
    else row++;
  }
  return false;
}

module.exports = { matrixSearch };
