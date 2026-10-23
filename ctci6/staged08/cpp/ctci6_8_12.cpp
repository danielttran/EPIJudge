#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
class Solution {
 public:
  std::vector<std::vector<int>> EightQueens() {
    std::vector<int> board(8);
    std::vector<std::vector<int>> result;
    std::function<void(int, int, int, int)> visit = [&](int row, int usedColumns, int usedDown,
                                                        int usedUp) {
      if (row == 8) {
        result.push_back(board);
        return;
      }
      for (int column = 0; column < 8; ++column) {
        int colBit = 1 << column, downBit = 1 << (row - column + 7), upBit = 1 << (row + column);
        if ((usedColumns & colBit) != 0 || (usedDown & downBit) != 0 || (usedUp & upBit) != 0)
          continue;
        board[row] = column;
        visit(row + 1, usedColumns | colBit, usedDown | downBit, usedUp | upBit);
      }
    };
    visit(0, 0, 0, 0);
    return result;
  }
};
