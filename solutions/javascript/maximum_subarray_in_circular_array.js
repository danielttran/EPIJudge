function maxSubarraySumInCircular(A) {
  let maximumSuffix = 0,
    minimumSuffix = 0,
    best = 0,
    worst = 0,
    total = 0;
  for (const value of A) {
    total += value;
    maximumSuffix = Math.max(0, maximumSuffix + value);
    best = Math.max(best, maximumSuffix);
    minimumSuffix = Math.min(0, minimumSuffix + value);
    worst = Math.min(worst, minimumSuffix);
  }
  return Math.max(best, total - worst);
}

module.exports = { maxSubarraySumInCircular };
