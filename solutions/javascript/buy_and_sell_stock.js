function buyAndSellStockOnce(prices) {
  let minimum = Infinity,
    profit = 0;
  for (const price of prices) {
    profit = Math.max(profit, price - minimum);
    minimum = Math.min(minimum, price);
  }
  return profit;
}

module.exports = { buyAndSellStockOnce };
