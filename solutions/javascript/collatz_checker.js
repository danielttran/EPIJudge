function testCollatzConjecture(n) {
  for (let start = 3n; start <= BigInt(n); start += 2n) {
    const seen = new Set();
    let value = start;
    while (value >= start) {
      if (seen.has(value)) return false;
      seen.add(value);
      value = value % 2n === 0n ? value / 2n : 3n * value + 1n;
    }
  }
  return true;
}

module.exports = { testCollatzConjecture };
