#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
#include <unordered_map>
#include <unordered_set>
class Solution {
 public:
  bool MatchesPattern(const std::string& pattern, const std::string& text) {
    if (pattern.empty())
      return text.empty();
    int countA = 0;
    for (char symbol : pattern)
      if (symbol == 'a')
        ++countA;
    int countB = static_cast<int>(pattern.size()) - countA, n = static_cast<int>(text.size()),
        maximum = countA ? n / countA : 0;
    for (int lengthA = 0; lengthA <= maximum; ++lengthA) {
      int remaining = n - countA * lengthA;
      if (countB == 0 ? remaining != 0 : remaining % countB != 0)
        continue;
      int lengthB = countB == 0 ? 0 : remaining / countB;
      std::string a, b;
      bool haveA = false, haveB = false, valid = true;
      int offset = 0;
      for (char symbol : pattern) {
        int length = symbol == 'a' ? lengthA : lengthB;
        auto part = text.substr(offset, length);
        if (symbol == 'a') {
          if (!haveA) {
            a = part;
            haveA = true;
          } else if (a != part) {
            valid = false;
            break;
          }
        } else {
          if (!haveB) {
            b = part;
            haveB = true;
          } else if (b != part) {
            valid = false;
            break;
          }
        }
        offset += length;
      }
      if (valid && offset == n)
        return true;
    }
    return false;
  }
};
