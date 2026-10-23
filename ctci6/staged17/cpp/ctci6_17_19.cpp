#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
class Solution {
 public:
  std::vector<int> MissingTwo(const std::vector<int>& values) {
    int n = static_cast<int>(values.size()) + 2, combined = 0;
    for (int value = 1; value <= n; ++value)
      combined ^= value;
    for (int value : values)
      combined ^= value;
    int bit = combined & -combined, first = 0, second = 0;
    for (int value = 1; value <= n; ++value) {
      if ((value & bit) != 0)
        first ^= value;
      else
        second ^= value;
    }
    for (int value : values) {
      if ((value & bit) != 0)
        first ^= value;
      else
        second ^= value;
    }
    return {std::min(first, second), std::max(first, second)};
  }
};
