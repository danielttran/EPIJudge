#include <algorithm>
#include <array>
#include <string>
#include <vector>
class Solution {
 public:
  void Rotate(std::vector<std::vector<int>>& matrix) {
    int n = static_cast<int>(matrix.size());
    for (int r = 0; r < n; ++r) {
      for (int c = r + 1; c < n; ++c) {
        int saved = matrix[r][c];
        matrix[r][c] = matrix[c][r];
        matrix[c][r] = saved;
      }
    }
    for (int r = 0; r < n; ++r) {
      for (int c = 0; c < n / 2; ++c) {
        int saved = matrix[r][c];
        matrix[r][c] = matrix[r][n - 1 - c];
        matrix[r][n - 1 - c] = saved;
      }
    }
  }
};
