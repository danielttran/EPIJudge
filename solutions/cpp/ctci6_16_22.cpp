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
  std::vector<std::string> LangtonBoard(int steps) {
    int width = 2 * steps + 1, row = 0, column = 0, direction = 0, minRow = 0, maxRow = 0,
        minColumn = 0, maxColumn = 0;
    std::unordered_set<int> black;
    const std::array<int, 4> dr = {0, 1, 0, -1}, dc = {1, 0, -1, 0};
    for (int turn = 0; turn < steps; ++turn) {
      int key = (row + steps) * width + column + steps;
      if (black.count(key)) {
        direction = (direction + 3) % 4;
        black.erase(key);
      } else {
        direction = (direction + 1) % 4;
        black.insert(key);
      }
      row += dr[direction];
      column += dc[direction];
      minRow = std::min(minRow, row);
      maxRow = std::max(maxRow, row);
      minColumn = std::min(minColumn, column);
      maxColumn = std::max(maxColumn, column);
    }
    std::vector<std::string> result;
    for (int r = minRow; r <= maxRow; ++r) {
      std::string line;
      for (int c = minColumn; c <= maxColumn; ++c)
        line += r == row && c == column                        ? std::string("RDLU")[direction]
                : black.count((r + steps) * width + c + steps) ? '#'
                                                               : '.';
      result.push_back(line);
    }
    return result;
  }
};
