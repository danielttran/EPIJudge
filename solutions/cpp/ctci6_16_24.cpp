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
  std::vector<std::vector<int>> PairsWithSum(const std::vector<int>& values, int target) {
    auto ordered = values;
    std::sort(ordered.begin(), ordered.end());
    std::vector<std::vector<int>> result;
    int left = 0, right = static_cast<int>(ordered.size()) - 1;
    while (left < right) {
      long long total = static_cast<long long>(ordered[left]) + ordered[right];
      if (total == target) {
        result.push_back({ordered[left], ordered[right]});
        ++left;
        --right;
      } else if (total < target)
        ++left;
      else
        --right;
    }
    return result;
  }
};
