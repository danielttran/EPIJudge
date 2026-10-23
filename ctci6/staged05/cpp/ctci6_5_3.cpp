#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
class Solution {
 public:
  int LongestOnesAfterFlip(int word) {
    std::uint32_t bits = static_cast<std::uint32_t>(word);
    int left = 0, zeros = 0, best = 0;
    for (int right = 0; right < 32; ++right) {
      if (((bits >> right) & 1) == 0)
        ++zeros;
      while (zeros > 1) {
        if (((bits >> left) & 1) == 0)
          --zeros;
        ++left;
      }
      best = std::max(best, right - left + 1);
    }
    return best;
  }
};
