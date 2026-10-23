#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
class Solution {
 public:
  int MaximumContiguousSum(const std::vector<int>& values) {
    int running = 0, best = 0;
    for (int value : values) {
      running = std::max(0, running + value);
      best = std::max(best, running);
    }
    return best;
  }
};
