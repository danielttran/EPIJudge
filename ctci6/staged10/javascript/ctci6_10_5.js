'use strict';
function SparseSearch(words, target) {
  if (target.length === 0) return -1;
  let low = 0,
    high = words.length - 1;
  while (low <= high) {
    let middle = low + Math.floor((high - low) / 2);
    if (words[middle].length === 0) {
      let left = middle - 1,
        right = middle + 1;
      while (true) {
        if (left < low && right > high) return -1;
        if (right <= high && words[right].length !== 0) {
          middle = right;
          break;
        }
        if (left >= low && words[left].length !== 0) {
          middle = left;
          break;
        }
        --left;
        ++right;
      }
    }
    if (words[middle] === target) return middle;
    if (words[middle] < target) low = middle + 1;
    else high = middle - 1;
  }
  return -1;
}
