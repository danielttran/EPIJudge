function generatePrimes(n) {
  const composite = Array(Math.max(0, n + 1)).fill(false),
    primes = [];
  for (let p = 2; p <= n; p++) {
    if (composite[p]) continue;
    primes.push(p);
    for (let multiple = p * p; multiple <= n; multiple += p)
      composite[multiple] = true;
  }
  return primes;
}

module.exports = { generatePrimes };
