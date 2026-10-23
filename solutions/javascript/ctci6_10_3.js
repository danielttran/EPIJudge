'use strict';
function SearchRotated(values, target) {
  let left = 0,
    right = values.length - 1;
  while (left <= right) {
    const middle = left + Math.floor((right - left) / 2);
    if (values[middle] === target) return middle;
    if (values[left] === values[middle] && values[middle] === values[right]) {
      ++left;
      --right;
    } else if (values[left] <= values[middle]) {
      if (values[left] <= target && target < values[middle]) right = middle - 1;
      else left = middle + 1;
    } else {
      if (values[middle] < target && target <= values[right]) left = middle + 1;
      else right = middle - 1;
    }
  }
  return -1;
}

module.exports = {SearchRotated};
