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
  std::vector<double> BisectSquares(const std::vector<std::vector<int>>& squares) {
    double x = squares[0][0] + squares[0][2] / 2.0, y = squares[0][1] + squares[0][2] / 2.0,
           dx = squares[1][0] + squares[1][2] / 2.0 - x,
           dy = squares[1][1] + squares[1][2] / 2.0 - y, other = 1;
    if (dx == 0 && dy == 0) {
      dy = 1;
      other = 0;
    }
    double scale = std::max(std::abs(dx), std::abs(dy)), first = squares[0][2] / (2.0 * scale),
           second = squares[1][2] / (2.0 * scale), start = std::min(-first, other - second),
           end = std::max(first, other + second);
    return {x + start * dx, y + start * dy, x + end * dx, y + end * dy};
  }
};
