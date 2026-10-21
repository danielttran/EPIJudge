function mergeTwoSortedArrays(A, m, B, n) {
  let first = m - 1,
    second = n - 1,
    output = m + n - 1;
  while (second >= 0) {
    if (first >= 0 && A[first] > B[second]) A[output--] = A[first--];
    else A[output--] = B[second--];
  }
  return A;
}

module.exports = { mergeTwoSortedArrays };
