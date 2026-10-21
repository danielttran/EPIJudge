function multiply(x, y) {
  function add(a, b) {
    while (b !== 0n) {
      const carry = (a & b) << 1n;
      a ^= b;
      b = carry;
    }
    return a;
  }
  let a = BigInt(x),
    b = BigInt(y),
    result = 0n;
  while (a !== 0n) {
    if (a & 1n) result = add(result, b);
    a >>= 1n;
    b <<= 1n;
  }
  return result;
}

module.exports = { multiply };
