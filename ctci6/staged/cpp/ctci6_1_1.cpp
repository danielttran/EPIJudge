#include <algorithm>
#include <array>
#include <string>
#include <vector>
class Solution {
 public:
  bool IsUnique(const std::string& text) {
    std::vector<bool> seen(128, false);
    for (int i = 0; i < static_cast<int>(text.size()); ++i) {
      int code = text[i];
      if (seen[code])
        return false;
      seen[code] = true;
    }
    return true;
  }
};
