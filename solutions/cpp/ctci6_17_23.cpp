#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
class Solution {
 public:
  std::vector<int> LargestBlackBorder(const std::vector<std::vector<int>>& matrix) {
    int n = static_cast<int>(matrix.size());
    std::vector<std::vector<int>> right(n, std::vector<int>(n)), down(n, std::vector<int>(n));
    for (int r = n - 1; r >= 0; --r) {
      for (int c = n - 1; c >= 0; --c) {
        if (matrix[r][c] == 0) {
          right[r][c] = 1 + (c + 1 < n ? right[r][c + 1] : 0);
          down[r][c] = 1 + (r + 1 < n ? down[r + 1][c] : 0);
        }
      }
    }
    for (int size = n; size >= 1; --size) {
      for (int r = 0; r + size <= n; ++r) {
        for (int c = 0; c + size <= n; ++c) {
          if (right[r][c] >= size && down[r][c] >= size && right[r + size - 1][c] >= size &&
              down[r][c + size - 1] >= size)
            return {r, c, size};
        }
      }
    }
    return {};
  }
};
