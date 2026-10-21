function squareRoot(x) {
  if (x === 0) return 0;
  let low = 0,
    high = Math.max(1, x);
  for (let step = 0; step < 1100; step++) {
    const middle = low + (high - low) / 2;
    if (middle === low || middle === high) break;
    if (middle <= x / middle) low = middle;
    else high = middle;
  }
  return low + (high - low) / 2;
}

module.exports = { squareRoot };
