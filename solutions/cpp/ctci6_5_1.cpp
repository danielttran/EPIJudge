#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
class Solution {
 public:
  int InsertBits(int word, int insert, int low, int high) {
    int width = high - low + 1;
    std::uint64_t mask = (1ULL << width) - 1ULL;
    std::uint64_t bits = static_cast<std::uint32_t>(word),
                  replacement = static_cast<std::uint32_t>(insert);
    std::uint64_t result = (bits & ~(mask << low)) | ((replacement & mask) << low);
    if (result >= 2147483648ULL)
      return static_cast<int>(static_cast<long long>(result) - 4294967296LL);
    return static_cast<int>(result);
  }
};
