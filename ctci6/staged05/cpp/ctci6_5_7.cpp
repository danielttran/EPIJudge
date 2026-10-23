#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
class Solution {
 public:
  int SwapAdjacentBits(int word) {
    std::uint32_t bits = static_cast<std::uint32_t>(word);
    std::uint32_t result = ((bits & 0x55555555u) << 1) | ((bits & 0xaaaaaaaau) >> 1);
    if (result >= 2147483648u)
      return static_cast<int>(static_cast<long long>(result) - 4294967296LL);
    return static_cast<int>(result);
  }
};
