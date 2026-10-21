function parity(x) {
  let bits = BigInt.asUintN(64, BigInt(x)),
    result = 0;
  while (bits !== 0n) {
    result ^= 1;
    bits &= bits - 1n;
  }
  return result;
}

module.exports = { parity };
