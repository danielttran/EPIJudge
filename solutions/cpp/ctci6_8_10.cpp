#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
class Solution {
 public:
  std::vector<std::vector<int>> PaintFill(std::vector<std::vector<int>>& screen, int row,
                                          int column, int newColor) {
    int rows = static_cast<int>(screen.size()),
        columns = rows == 0 ? 0 : static_cast<int>(screen[0].size());
    if (row < 0 || row >= rows || column < 0 || column >= columns)
      return screen;
    int oldColor = screen[row][column];
    if (oldColor == newColor)
      return screen;
    std::vector<std::pair<int, int>> work{{row, column}};
    screen[row][column] = newColor;
    int dr[] = {-1, 1, 0, 0}, dc[] = {0, 0, -1, 1};
    while (!work.empty()) {
      auto [r, c] = work.back();
      work.pop_back();
      for (int i = 0; i < 4; ++i) {
        int nr = r + dr[i], nc = c + dc[i];
        if (nr >= 0 && nr < rows && nc >= 0 && nc < columns && screen[nr][nc] == oldColor) {
          screen[nr][nc] = newColor;
          work.push_back({nr, nc});
        }
      }
    }
    return screen;
  }
};
