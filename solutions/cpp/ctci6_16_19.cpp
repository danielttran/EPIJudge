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
  std::vector<int> PondSizes(const std::vector<std::vector<int>>& land) {
    int rows = static_cast<int>(land.size()),
        columns = rows == 0 ? 0 : static_cast<int>(land[0].size());
    std::vector<std::vector<bool>> seen(rows, std::vector<bool>(columns));
    std::vector<int> sizes;
    for (int row = 0; row < rows; ++row) {
      for (int column = 0; column < columns; ++column) {
        if (land[row][column] != 0 || seen[row][column])
          continue;
        seen[row][column] = true;
        std::vector<std::pair<int, int>> work{{row, column}};
        int size = 0;
        while (!work.empty()) {
          auto [r, c] = work.back();
          work.pop_back();
          ++size;
          for (int dr = -1; dr <= 1; ++dr) {
            for (int dc = -1; dc <= 1; ++dc) {
              if (dr == 0 && dc == 0)
                continue;
              int nr = r + dr, nc = c + dc;
              if (nr >= 0 && nr < rows && nc >= 0 && nc < columns && land[nr][nc] == 0 &&
                  !seen[nr][nc]) {
                seen[nr][nc] = true;
                work.push_back({nr, nc});
              }
            }
          }
        }
        sizes.push_back(size);
      }
    }
    std::sort(sizes.begin(), sizes.end());
    return sizes;
  }
};
