function squareRoot(k) {
  let low = 0,
    high = k,
    result = 0;
  while (low <= high) {
    const middle = low + Math.floor((high - low) / 2);
    if (middle === 0 || middle <= Math.floor(k / middle)) {
      result = middle;
      low = middle + 1;
    } else high = middle - 1;
  }
  return result;
}

module.exports = { squareRoot };
