#include <algorithm>
#include <array>
#include <string>
#include <vector>
class Solution {
 public:
  bool PalindromePermutation(const std::string& text) {
    std::array<int, 128> counts{};
    for (int i = 0; i < static_cast<int>(text.size()); ++i) {
      int code = text[i];
      if (code >= 65 && code <= 90)
        code += 32;
      if (code >= 97 && code <= 122)
        ++counts[code];
    }
    int odd = 0;
    for (int code = 97; code <= 122; ++code)
      odd += counts[code] % 2;
    return odd <= 1;
  }
};
