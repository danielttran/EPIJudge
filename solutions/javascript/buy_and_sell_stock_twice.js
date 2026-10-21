function buyAndSellStockTwice(prices) {
  let firstBuy = -Infinity,
    firstSell = 0,
    secondBuy = -Infinity,
    secondSell = 0;
  for (const price of prices) {
    secondSell = Math.max(secondSell, secondBuy + price);
    secondBuy = Math.max(secondBuy, firstSell - price);
    firstSell = Math.max(firstSell, firstBuy + price);
    firstBuy = Math.max(firstBuy, -price);
  }
  return secondSell;
}

module.exports = { buyAndSellStockTwice };
