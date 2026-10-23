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
  long long SmallestDifference(const std::vector<int>& first, const std::vector<int>& second) {
    if (first.empty() || second.empty())
      return -1;
    auto a = first, b = second;
    std::sort(a.begin(), a.end());
    std::sort(b.begin(), b.end());
    size_t i = 0, j = 0;
    long long best = 4294967295LL;
    while (i < a.size() && j < b.size()) {
      long long difference = static_cast<long long>(a[i]) - b[j];
      best = std::min(best, difference < 0 ? -difference : difference);
      if (difference == 0)
        return 0;
      if (difference < 0)
        ++i;
      else
        ++j;
    }
    return best;
  }
};
