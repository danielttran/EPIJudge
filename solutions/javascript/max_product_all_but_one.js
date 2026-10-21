function findBiggestNMinusOneProduct(A) {
  if (!A.length) return 0;
  let product = 1n,
    zeroes = 0;
  for (const value of A) {
    if (value === 0) zeroes++;
    else product *= BigInt(value);
  }
  if (zeroes > 1) return 0;
  if (zeroes === 1)
    return Number(A.length === 1 ? product : product > 0n ? product : 0n);
  let best = product / BigInt(A[0]);
  for (const value of A) {
    const candidate = product / BigInt(value);
    if (candidate > best) best = candidate;
  }
  return Number(best);
}

module.exports = { findBiggestNMinusOneProduct };
