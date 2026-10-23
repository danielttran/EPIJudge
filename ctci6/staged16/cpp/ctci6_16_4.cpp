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
  int TicTacWinner(const std::vector<std::vector<int>>& board) {
    int n = static_cast<int>(board.size());
    if (n == 0)
      return 0;
    for (int i = 0; i < n; ++i) {
      int row = board[i][0], column = board[0][i];
      for (int j = 0; j < n; ++j) {
        if (board[i][j] != row)
          row = 0;
        if (board[j][i] != column)
          column = 0;
      }
      if (row != 0)
        return row;
      if (column != 0)
        return column;
    }
    int main = board[0][0], other = board[0][n - 1];
    for (int i = 0; i < n; ++i) {
      if (board[i][i] != main)
        main = 0;
      if (board[i][n - 1 - i] != other)
        other = 0;
    }
    if (main != 0)
      return main;
    return other;
  }
};
