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
  int MaximumWithoutComparison(int first, int second) {
    auto a = static_cast<std::uint32_t>(first), b = static_cast<std::uint32_t>(second);
    int negativeFirst = a >> 31, negativeSecond = b >> 31, negativeDifference = (a - b) >> 31,
        different = negativeFirst ^ negativeSecond,
        chooseFirst = different * (negativeFirst ^ 1) + (different ^ 1) * (negativeDifference ^ 1);
    return first * chooseFirst + second * (chooseFirst ^ 1);
  }
};
