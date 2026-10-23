#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
class Solution {
 public:
  std::vector<int> MajorityElement(const std::vector<int>& values) {
    int candidate = 0, balance = 0;
    for (int value : values) {
      if (balance == 0)
        candidate = value;
      balance += value == candidate ? 1 : -1;
    }
    int count = 0;
    for (int value : values) {
      if (value == candidate)
        ++count;
    }
    if (count > static_cast<int>(values.size()) / 2)
      return {candidate};
    return {};
  }
};
