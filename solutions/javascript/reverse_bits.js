function reverseBits(x) {
  let source = BigInt.asUintN(64, BigInt(x)),
    result = 0n;
  for (let i = 0; i < 64; i++) {
    result = (result << 1n) | (source & 1n);
    source >>= 1n;
  }
  return BigInt.asIntN(64, result);
}

module.exports = { reverseBits };
