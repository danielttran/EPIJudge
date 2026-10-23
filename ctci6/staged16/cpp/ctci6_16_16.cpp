#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
#include <unordered_map>
#include <unordered_set>
class Solution {
 public:
  std::vector<int> ShortestSortWindow(const std::vector<int>& values) {
    int n = static_cast<int>(values.size());
    if (n == 0)
      return {-1, -1};
    int right = -1, maximum = values[0];
    for (int i = 0; i < n; ++i) {
      if (values[i] < maximum)
        right = i;
      maximum = std::max(maximum, values[i]);
    }
    if (right == -1)
      return {-1, -1};
    int left = -1, minimum = values[n - 1];
    for (int i = n - 1; i >= 0; --i) {
      if (values[i] > minimum)
        left = i;
      minimum = std::min(minimum, values[i]);
    }
    return {left, right};
  }
};
