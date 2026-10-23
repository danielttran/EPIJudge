#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
class Solution {
 public:
  int CountBitChanges(int first, int second) {
    std::uint32_t difference =
        static_cast<std::uint32_t>(first) ^ static_cast<std::uint32_t>(second);
    int count = 0;
    while (difference != 0) {
      difference &= difference - 1;
      ++count;
    }
    return count;
  }
};
