function swapBits(x, i, j) {
  let bits = BigInt.asUintN(64, BigInt(x));
  i = BigInt(i);
  j = BigInt(j);
  if (((bits >> i) & 1n) !== ((bits >> j) & 1n)) bits ^= (1n << i) | (1n << j);
  return BigInt.asIntN(64, bits);
}

module.exports = { swapBits };
