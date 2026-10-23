#include <algorithm>
#include <array>
#include <string>
#include <vector>
class Solution {
 public:
  bool CheckPermutation(const std::string& first, const std::string& second) {
    if (static_cast<int>(first.size()) != static_cast<int>(second.size()))
      return false;
    std::array<int, 128> counts{};
    for (int i = 0; i < static_cast<int>(first.size()); ++i)
      ++counts[first[i]];
    for (int i = 0; i < static_cast<int>(second.size()); ++i) {
      int code = second[i];
      --counts[code];
      if (counts[code] < 0)
        return false;
    }
    return true;
  }
};
