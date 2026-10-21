function closestIntSameBitCount(x) {
  x = BigInt(x);
  for (let bit = 0n; bit < 62n; bit++)
    if (((x >> bit) & 1n) !== ((x >> (bit + 1n)) & 1n))
      return x ^ (1n << bit) ^ (1n << (bit + 1n));
  throw new RangeError("No distinct nonnegative value has this bit count");
}

module.exports = { closestIntSameBitCount };
