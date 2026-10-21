function binarySearchUnknownLength(A, k) {
  function read(index) {
    return A[index];
  }
  let left = 0,
    right = 1;
  while (read(right) !== undefined && read(right) < k) {
    left = right + 1;
    right = right * 2 + 1;
  }
  while (left <= right) {
    const middle = left + Math.floor((right - left) / 2),
      value = read(middle);
    if (value === undefined || value > k) right = middle - 1;
    else if (value < k) left = middle + 1;
    else return middle;
  }
  return -1;
}

module.exports = { binarySearchUnknownLength };
