function intersectTwoSortedArrays(A, B) {
  const result = [];
  let i = 0,
    j = 0;
  while (i < A.length && j < B.length) {
    if (A[i] < B[j]) i++;
    else if (A[i] > B[j]) j++;
    else {
      if (!result.length || result.at(-1) !== A[i]) result.push(A[i]);
      i++;
      j++;
    }
  }
  return result;
}

module.exports = { intersectTwoSortedArrays };
