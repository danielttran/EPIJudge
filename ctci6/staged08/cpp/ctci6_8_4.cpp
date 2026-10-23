#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
class Solution {
 public:
  std::vector<std::vector<int>> PowerSet(const std::vector<int>& values) {
    std::vector<std::vector<int>> result(1);
    for (int value : values) {
      auto original = result.size();
      for (std::size_t i = 0; i < original; ++i) {
        auto subset = result[i];
        subset.push_back(value);
        result.push_back(std::move(subset));
      }
    }
    return result;
  }
};
