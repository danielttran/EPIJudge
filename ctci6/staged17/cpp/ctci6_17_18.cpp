#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
#include <unordered_map>
class Solution {
 public:
  std::vector<int> ShortestCoveringRange(const std::vector<int>& big,
                                         const std::vector<int>& small) {
    if (static_cast<int>(small.size()) == 0)
      return {-1, -1};
    std::unordered_map<int, int> counts;
    for (int value : small)
      counts[value] = 0;
    int missing = static_cast<int>(small.size()), left = 0, start = -1, end = -1;
    for (int right = 0; right < static_cast<int>(big.size()); ++right) {
      int value = big[right];
      if (counts.find(value) != counts.end()) {
        if (counts[value] == 0)
          --missing;
        ++counts[value];
      }
      while (missing == 0) {
        if (start == -1 || right - left < end - start) {
          start = left;
          end = right;
        }
        int removed = big[left];
        if (counts.find(removed) != counts.end()) {
          --counts[removed];
          if (counts[removed] == 0)
            ++missing;
        }
        ++left;
      }
    }
    return {start, end};
  }
};
