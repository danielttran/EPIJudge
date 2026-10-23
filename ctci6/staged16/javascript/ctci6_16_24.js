'use strict';
function PairsWithSum(values, target) {
  const ordered = values.slice().sort((a, b) => a - b),
    result = [];
  let left = 0,
    right = ordered.length - 1;
  while (left < right) {
    const total = ordered[left] + ordered[right];
    if (total === target) {
      result.push([ordered[left], ordered[right]]);
      ++left;
      --right;
    } else if (total < target) ++left;
    else --right;
  }
  return result;
}
