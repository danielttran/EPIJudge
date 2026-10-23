#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
class Solution {
 public:
  std::vector<int> MaximumSubmatrix(const std::vector<std::vector<int>>& matrix) {
    int rows = static_cast<int>(matrix.size()),
        columns = rows == 0 ? 0 : static_cast<int>(matrix[0].size());
    if (rows == 0 || columns == 0)
      return {};
    int best = -2147483648;
    std::vector<int> answer(5);
    for (int top = 0; top < rows; ++top) {
      std::vector<int> totals(columns);
      for (int bottom = top; bottom < rows; ++bottom) {
        int running = 0, start = 0;
        for (int c = 0; c < columns; ++c) {
          totals[c] += matrix[bottom][c];
          if (running < 0) {
            running = totals[c];
            start = c;
          } else
            running += totals[c];
          if (running > best) {
            best = running;
            answer = {best, top, start, bottom, c};
          }
        }
      }
    }
    return answer;
  }
};
