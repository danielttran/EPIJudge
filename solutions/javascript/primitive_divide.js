function divide(x, y) {
  if (y <= 0) throw new RangeError("Positive divisor required");
  let remaining = BigInt(x),
    quotient = 0n;
  for (let bit = 30n; bit >= 0n; bit--) {
    const part = BigInt(y) << bit;
    if (part <= remaining) {
      remaining -= part;
      quotient |= 1n << bit;
    }
  }
  return Number(quotient);
}

module.exports = { divide };
