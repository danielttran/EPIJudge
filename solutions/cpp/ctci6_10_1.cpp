#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
class Solution {
 public:
  std::vector<int> MergeSortedIntoFirst(std::vector<int>& first, int realCount,
                                        const std::vector<int>& second) {
    int a = realCount - 1, b = static_cast<int>(second.size()) - 1,
        write = static_cast<int>(first.size()) - 1;
    while (b >= 0) {
      if (a >= 0 && first[a] > second[b])
        first[write--] = first[a--];
      else
        first[write--] = second[b--];
    }
    return first;
  }
};
