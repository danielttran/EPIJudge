#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
class Solution {
 public:
  std::vector<int> RepeatedOccurrences(const std::vector<int>& values) {
    std::array<unsigned char, 4000> bits{};
    int count = 0;
    for (int value : values) {
      int slot = (value - 1) >> 3, mask = 1 << ((value - 1) & 7);
      if ((bits[slot] & mask) != 0)
        ++count;
      else
        bits[slot] = static_cast<unsigned char>(bits[slot] | mask);
    }
    std::vector<int> result(count);
    bits.fill(0);
    int write = 0;
    for (int value : values) {
      int slot = (value - 1) >> 3, mask = 1 << ((value - 1) & 7);
      if ((bits[slot] & mask) != 0)
        result[write++] = value;
      else
        bits[slot] = static_cast<unsigned char>(bits[slot] | mask);
    }
    return result;
  }
};
