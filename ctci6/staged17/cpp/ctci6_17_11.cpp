#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
class Solution {
 public:
  int WordDistance(const std::vector<std::string>& words, const std::string& first,
                   const std::string& second) {
    int lastFirst = -1, lastSecond = -1, best = static_cast<int>(words.size()) + 1;
    for (int i = 0; i < static_cast<int>(words.size()); ++i) {
      if (words[i] == first) {
        lastFirst = i;
        if (lastSecond >= 0)
          best = std::min(best, i - lastSecond);
      } else if (words[i] == second) {
        lastSecond = i;
        if (lastFirst >= 0)
          best = std::min(best, i - lastFirst);
      }
    }
    return best == static_cast<int>(words.size()) + 1 ? -1 : best;
  }
};
