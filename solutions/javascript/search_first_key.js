function searchFirstOfK(A, k) {
  let left = 0,
    right = A.length;
  while (left < right) {
    const middle = left + Math.floor((right - left) / 2);
    if (A[middle] < k) left = middle + 1;
    else right = middle;
  }
  return left < A.length && A[left] === k ? left : -1;
}

module.exports = { searchFirstOfK };
