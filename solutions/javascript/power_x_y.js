function power(x, y) {
  let exponent = BigInt(y);
  if (exponent < 0n) {
    x = 1 / x;
    exponent = -exponent;
  }
  let result = 1;
  while (exponent > 0n) {
    if (exponent & 1n) result *= x;
    x *= x;
    exponent >>= 1n;
  }
  return result;
}

module.exports = { power };
