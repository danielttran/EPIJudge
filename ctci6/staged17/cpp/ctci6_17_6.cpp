#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
class Solution {
 public:
  int CountDigitTwos(int n) {
    std::int64_t total = 0;
    for (std::int64_t place = 1; place <= n; place *= 10) {
      std::int64_t high = n / (place * 10), digit = (n / place) % 10, low = n % place;
      total += high * place;
      if (digit == 2)
        total += low + 1;
      else if (digit > 2)
        total += place;
    }
    return static_cast<int>(total);
  }
};
