function findKthLargest(k, A) {
  const target = k - 1;
  let low = 0,
    high = A.length - 1;
  while (low <= high) {
    const pivot = A[low + Math.floor((high - low) / 2)];
    let greater = low,
      scan = low,
      smaller = high;
    while (scan <= smaller) {
      if (A[scan] > pivot) {
        [A[greater], A[scan]] = [A[scan], A[greater]];
        greater++;
        scan++;
      } else if (A[scan] < pivot) {
        [A[scan], A[smaller]] = [A[smaller], A[scan]];
        smaller--;
      } else scan++;
    }
    if (target < greater) high = greater - 1;
    else if (target > smaller) low = smaller + 1;
    else return A[target];
  }
  throw new RangeError("Invalid rank");
}

module.exports = { findKthLargest };
