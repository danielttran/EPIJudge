function computeBinomialCoefficient(n, k) {
  if (k < 0 || k > n) return 0;
  k = Math.min(k, n - k);
  let result = 1n;
  for (let i = 1; i <= k; i++)
    result = (result * BigInt(n - k + i)) / BigInt(i);
  return Number(result);
}

module.exports = { computeBinomialCoefficient };
