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
  std::vector<int> BestLine(const std::vector<std::vector<int>>& points) {
    if (points.empty())
      return {};
    auto gcd = [](int a, int b) {
      while (b != 0) {
        int next = a % b;
        a = b;
        b = next;
      }
      return a;
    };
    std::vector<int> best{1, 0, -points[0][0]};
    int bestCount = 0;
    for (size_t anchor = 0; anchor < points.size(); ++anchor) {
      std::unordered_map<int, int> groups;
      int duplicates = 0, x = points[anchor][0], y = points[anchor][1];
      for (size_t other = anchor + 1; other < points.size(); ++other) {
        int dx = points[other][0] - x, dy = points[other][1] - y;
        if (dx == 0 && dy == 0) {
          ++duplicates;
          continue;
        }
        int divisor = gcd(dx < 0 ? -dx : dx, dy < 0 ? -dy : dy);
        dx /= divisor;
        dy /= divisor;
        if (dx < 0 || (dx == 0 && dy < 0)) {
          dx = -dx;
          dy = -dy;
        }
        ++groups[(dy + 2000) * 4001 + dx];
      }
      for (const auto& entry : groups)
        if (entry.second + duplicates + 1 > bestCount) {
          bestCount = entry.second + duplicates + 1;
          int a = entry.first / 4001 - 2000, b = -(entry.first % 4001), c = -a * x - b * y;
          if (a < 0 || (a == 0 && b < 0)) {
            a = -a;
            b = -b;
            c = -c;
          }
          best = {a, b, c};
        }
    }
    return best;
  }
};
