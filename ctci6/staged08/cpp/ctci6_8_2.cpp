#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
class Solution {
 public:
  std::vector<std::vector<int>> FindRobotPath(const std::vector<std::vector<int>>& grid) {
    int rows = static_cast<int>(grid.size()),
        columns = rows == 0 ? 0 : static_cast<int>(grid[0].size());
    if (rows == 0 || columns == 0) {
      return {};
    }
    std::vector<std::vector<int>> parent(rows, std::vector<int>(columns)), path;
    for (int r = 0; r < rows; ++r) {
      for (int c = 0; c < columns; ++c) {
        if (grid[r][c] == 0)
          continue;
        if (r == 0 && c == 0)
          parent[r][c] = 3;
        else if (r > 0 && parent[r - 1][c] != 0)
          parent[r][c] = 1;
        else if (c > 0 && parent[r][c - 1] != 0)
          parent[r][c] = 2;
      }
    }
    if (parent[rows - 1][columns - 1] == 0) {
      return {};
    }
    int row = rows - 1, col = columns - 1;
    while (true) {
      path.push_back({row, col});
      if (row == 0 && col == 0)
        break;
      if (parent[row][col] == 1)
        --row;
      else
        --col;
    }
    std::reverse(path.begin(), path.end());
    return path;
  }
};
