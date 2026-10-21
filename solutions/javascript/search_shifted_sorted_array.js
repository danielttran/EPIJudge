function searchSmallest(A) {
  let left = 0,
    right = A.length - 1;
  while (left < right) {
    const middle = left + Math.floor((right - left) / 2);
    if (A[middle] > A[right]) left = middle + 1;
    else right = middle;
  }
  return A.length ? left : -1;
}

module.exports = { searchSmallest };
