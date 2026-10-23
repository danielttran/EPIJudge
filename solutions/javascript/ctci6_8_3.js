'use strict';
function FindMagicIndex(values, distinctValues) {
  if (distinctValues) {
    let low = 0,
      high = values.length - 1;
    while (low <= high) {
      const middle = low + Math.floor((high - low) / 2);
      if (values[middle] === middle) return middle;
      if (values[middle] > middle) high = middle - 1;
      else low = middle + 1;
    }
    return -1;
  }
  function search(low, high) {
    if (low > high) return -1;
    const middle = low + Math.floor((high - low) / 2),
      value = values[middle];
    if (value === middle) return middle;
    const left = search(low, Math.min(middle - 1, value));
    return left !== -1 ? left : search(Math.max(middle + 1, value), high);
  }
  return search(0, values.length - 1);
}

module.exports = {FindMagicIndex};
