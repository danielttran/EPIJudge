#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
class Solution {
 public:
  int MaximumMassageMinutes(const std::vector<int>& appointments) {
    int oneBack = 0, twoBack = 0;
    for (int duration : appointments) {
      int current = std::max(oneBack, duration + twoBack);
      twoBack = oneBack;
      oneBack = current;
    }
    return oneBack;
  }
};
