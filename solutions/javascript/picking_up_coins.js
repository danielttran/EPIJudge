function maximumRevenue(coins) {
  const n = coins.length;
  if (!n) return 0;
  const best = Array.from({ length: n }, () => Array(n).fill(0));
  const value = (l, r) => (l > r ? 0 : best[l][r]);
  for (let size = 1; size <= n; size++)
    for (let l = 0; l + size <= n; l++) {
      const r = l + size - 1;
      best[l][r] = Math.max(
        coins[l] + Math.min(value(l + 2, r), value(l + 1, r - 1)),
        coins[r] + Math.min(value(l + 1, r - 1), value(l, r - 2)),
      );
    }
  return best[0][n - 1];
}

module.exports = { maximumRevenue };
