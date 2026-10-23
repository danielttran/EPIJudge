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
  std::vector<int> SumSwap(const std::vector<int>& first, const std::vector<int>& second) {
    long long difference = 0;
    for (int value : first)
      difference += value;
    for (int value : second)
      difference -= value;
    if (difference % 2 != 0)
      return {};
    long long half = difference / 2;
    std::unordered_set<int> contents(second.begin(), second.end());
    for (int value : first) {
      long long required = static_cast<long long>(value) - half;
      if (required >= -2147483648LL && required <= 2147483647LL &&
          contents.count(static_cast<int>(required)))
        return {value, static_cast<int>(required)};
    }
    return {};
  }
};
