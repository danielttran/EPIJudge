function numberOfWays(n, m) {
  if (n <= 0 || m <= 0) return 0;
  const ways = Array(Math.min(n, m)).fill(1);
  for (let r = 1; r < Math.max(n, m); r++)
    for (let c = 1; c < ways.length; c++) ways[c] += ways[c - 1];
  return ways.at(-1);
}

module.exports = { numberOfWays };
