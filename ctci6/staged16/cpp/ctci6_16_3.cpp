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
  std::vector<double> SegmentIntersection(const std::vector<std::vector<int>>& endpoints) {
    const auto& a = endpoints[0];
    const auto& b = endpoints[1];
    const auto& c = endpoints[2];
    const auto& d = endpoints[3];
    int rx = b[0] - a[0], ry = b[1] - a[1], sx = d[0] - c[0], sy = d[1] - c[1], qx = c[0] - a[0],
        qy = c[1] - a[1], denominator = rx * sy - ry * sx;
    if (denominator != 0) {
      int first = qx * sy - qy * sx, second = qx * ry - qy * rx;
      if (denominator < 0) {
        denominator = -denominator;
        first = -first;
        second = -second;
      }
      if (first >= 0 && first <= denominator && second >= 0 && second <= denominator) {
        double t = (double)first / denominator;
        return {a[0] + t * rx, a[1] + t * ry};
      }
      return {};
    }
    auto contains = [](const std::vector<int>& start, const std::vector<int>& end,
                       const std::vector<int>& point) {
      return (end[0] - start[0]) * (point[1] - start[1]) ==
                 (end[1] - start[1]) * (point[0] - start[0]) &&
             point[0] >= std::min(start[0], end[0]) && point[0] <= std::max(start[0], end[0]) &&
             point[1] >= std::min(start[1], end[1]) && point[1] <= std::max(start[1], end[1]);
    };
    for (const auto& point : endpoints)
      if (contains(a, b, point) && contains(c, d, point))
        return {(double)point[0], (double)point[1]};
    return {};
  }
};
