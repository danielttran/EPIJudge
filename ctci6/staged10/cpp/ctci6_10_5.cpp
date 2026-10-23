#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
class Solution {
 public:
  int SparseSearch(const std::vector<std::string>& words, const std::string& target) {
    if (target.empty())
      return -1;
    int low = 0, high = static_cast<int>(words.size()) - 1;
    while (low <= high) {
      int middle = low + (high - low) / 2;
      if (words[middle].empty()) {
        int left = middle - 1, right = middle + 1;
        while (true) {
          if (left < low && right > high)
            return -1;
          if (right <= high && !(words[right].empty())) {
            middle = right;
            break;
          }
          if (left >= low && !(words[left].empty())) {
            middle = left;
            break;
          }
          --left;
          ++right;
        }
      }
      int comparison = words[middle].compare(target);
      if (comparison == 0)
        return middle;
      if (comparison < 0)
        low = middle + 1;
      else
        high = middle - 1;
    }
    return -1;
  }
};
