function searchEntryEqualToItsIndex(values) {
  let left = 0,
    right = values.length - 1;
  while (left <= right) {
    const middle = left + Math.floor((right - left) / 2),
      difference = values[middle] - middle;
    if (difference === 0) return middle;
    if (difference < 0) left = middle + 1;
    else right = middle - 1;
  }
  return -1;
}

module.exports = { searchEntryEqualToItsIndex };
