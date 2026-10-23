#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
#include <iterator>
#include <stdexcept>
class Solution {
 public:
  std::vector<std::vector<int>> PlayOthello(int size,
                                            const std::vector<std::vector<int>>& actions) {
    std::vector<std::vector<int>> board(size, std::vector<int>(size)), trace;
    int middle = size / 2;
    board[middle - 1][middle - 1] = board[middle][middle] = 2;
    board[middle - 1][middle] = board[middle][middle - 1] = 1;
    auto captures = [&](int row, int column, int color) {
      std::vector<std::pair<int, int>> result;
      if (row < 0 || row >= size || column < 0 || column >= size || board[row][column] != 0)
        return result;
      for (int dr = -1; dr <= 1; ++dr)
        for (int dc = -1; dc <= 1; ++dc) {
          if (dr == 0 && dc == 0)
            continue;
          int r = row + dr, c = column + dc;
          std::vector<std::pair<int, int>> path;
          while (r >= 0 && r < size && c >= 0 && c < size && board[r][c] == 3 - color) {
            path.push_back({r, c});
            r += dr;
            c += dc;
          }
          if (!path.empty() && r >= 0 && r < size && c >= 0 && c < size && board[r][c] == color)
            result.insert(result.end(), path.begin(), path.end());
        }
      return result;
    };
    auto canMove = [&](int color) {
      for (int r = 0; r < size; ++r)
        for (int c = 0; c < size; ++c)
          if (!captures(r, c, color).empty())
            return true;
      return false;
    };
    int turn = canMove(1) ? 1 : 0;
    auto snapshot = [&](int accepted) {
      int black = 0, white = 0;
      for (const auto& row : board)
        for (int v : row) {
          black += v == 1;
          white += v == 2;
        }
      std::vector<int> result{turn, accepted, black, white};
      for (const auto& row : board)
        result.insert(result.end(), row.begin(), row.end());
      trace.push_back(std::move(result));
    };
    snapshot(0);
    for (const auto& action : actions) {
      int row = action[0], column = action[1], color = action[2], accepted = 0;
      if (turn && color == turn) {
        auto flipped = captures(row, column, color);
        if (!flipped.empty()) {
          board[row][column] = color;
          for (auto [r, c] : flipped)
            board[r][c] = color;
          accepted = 1;
          turn = canMove(3 - color) ? 3 - color : canMove(color) ? color : 0;
        }
      }
      snapshot(accepted);
    }
    return trace;
  }
};
