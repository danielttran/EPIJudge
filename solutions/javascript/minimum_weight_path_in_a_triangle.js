function minimumPathWeight(triangle) {
  if (!triangle.length) return 0;
  const costs = triangle.at(-1).slice();
  for (let r = triangle.length - 2; r >= 0; r--)
    for (let c = 0; c <= r; c++)
      costs[c] = triangle[r][c] + Math.min(costs[c], costs[c + 1]);
  return costs[0];
}

module.exports = { minimumPathWeight };
