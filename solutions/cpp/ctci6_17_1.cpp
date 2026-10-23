#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
#include <cstring>
class Solution {
 public:
  int AddWithoutArithmetic(int first, int second) {
    auto a = static_cast<std::uint32_t>(first), b = static_cast<std::uint32_t>(second);
    while (b != 0) {
      std::uint32_t carry = (a & b) << 1;
      a ^= b;
      b = carry;
    }
    std::int32_t result;
    std::memcpy(&result, &a, sizeof(result));
    return result;
  }
};
