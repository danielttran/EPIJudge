function buyAndSellStockKTimes(prices, k) {
  if (k <= 0 || prices.length < 2) return 0;
  if (k >= Math.floor(prices.length / 2)) {
    let total = 0;
    for (let i = 1; i < prices.length; i++)
      total += Math.max(0, prices[i] - prices[i - 1]);
    return total;
  }
  const holding = Array(k + 1).fill(-Infinity),
    sold = Array(k + 1).fill(0);
  for (const price of prices)
    for (let transaction = k; transaction >= 1; transaction--) {
      sold[transaction] = Math.max(
        sold[transaction],
        holding[transaction] + price,
      );
      holding[transaction] = Math.max(
        holding[transaction],
        sold[transaction - 1] - price,
      );
    }
  return sold[k];
}

module.exports = { buyAndSellStockKTimes };
