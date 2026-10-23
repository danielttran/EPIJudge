#include <algorithm>
#include <array>
#include <string>
#include <vector>
class Solution {
 public:
  void ZeroMatrix(std::vector<std::vector<int>>& matrix) {
    int rows = static_cast<int>(matrix.size());
    if (rows == 0)
      return;
    int cols = static_cast<int>(matrix[0].size());
    std::vector<bool> zeroRows(rows, false);
    std::vector<bool> zeroCols(cols, false);
    for (int r = 0; r < rows; ++r) {
      for (int c = 0; c < cols; ++c) {
        if (matrix[r][c] == 0) {
          zeroRows[r] = true;
          zeroCols[c] = true;
        }
      }
    }
    for (int r = 0; r < rows; ++r) {
      for (int c = 0; c < cols; ++c) {
        if (zeroRows[r] || zeroCols[c])
          matrix[r][c] = 0;
      }
    }
  }
};
