#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
class Solution {
 public:
  int CountCoinCombinations(int amount) {
    std::vector<int> ways(amount + 1);
    ways[0] = 1;
    for (int coin : std::array<int, 4>{1, 5, 10, 25}) {
      for (int value = coin; value <= amount; ++value)
        ways[value] += ways[value - coin];
    }
    return ways[amount];
  }
};
