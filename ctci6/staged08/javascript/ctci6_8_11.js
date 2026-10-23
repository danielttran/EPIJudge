'use strict';
function CountCoinCombinations(amount) {
  const ways = Array(amount + 1).fill(0);
  ways[0] = 1;
  for (const coin of [1, 5, 10, 25]) {
    for (let value = coin; value <= amount; ++value) ways[value] += ways[value - coin];
  }
  return ways[amount];
}
