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
  std::vector<std::vector<int>> PlayMinesweeper(const std::vector<std::vector<int>>& bombs,
                                                const std::vector<std::vector<int>>& actions) {
    int rows = bombs.size(), columns = bombs[0].size(), safe = 0, state = 0;
    for (const auto& row : bombs)
      for (int v : row)
        if (v == 0)
          ++safe;
    std::vector<std::vector<int>> visible(rows, std::vector<int>(columns, 9)), trace;
    auto snapshot = [&](int accepted) {
      std::vector<int> result{state, accepted};
      for (const auto& row : visible)
        result.insert(result.end(), row.begin(), row.end());
      trace.push_back(std::move(result));
    };
    auto expose = [&](int row, int column, std::vector<std::pair<int, int>>& queue) {
      if (visible[row][column] != 9 || bombs[row][column])
        return;
      int number = 0;
      for (int r = std::max(0, row - 1); r < std::min(rows, row + 2); ++r)
        for (int c = std::max(0, column - 1); c < std::min(columns, column + 2); ++c)
          number += bombs[r][c];
      visible[row][column] = number;
      --safe;
      if (number == 0)
        queue.push_back({row, column});
    };
    snapshot(0);
    for (const auto& action : actions) {
      int row = action[0], column = action[1], kind = action[2], accepted = 0;
      if (state == 0 && row >= 0 && row < rows && column >= 0 && column < columns) {
        if (kind == 1 && (visible[row][column] == 9 || visible[row][column] == 10)) {
          visible[row][column] = 19 - visible[row][column];
          accepted = 1;
        } else if (kind == 0 && visible[row][column] == 9) {
          accepted = 1;
          if (bombs[row][column]) {
            visible[row][column] = 11;
            state = 2;
          } else {
            std::vector<std::pair<int, int>> queue;
            expose(row, column, queue);
            for (size_t head = 0; head < queue.size(); ++head) {
              auto [r, c] = queue[head];
              for (int nr = std::max(0, r - 1); nr < std::min(rows, r + 2); ++nr)
                for (int nc = std::max(0, c - 1); nc < std::min(columns, c + 2); ++nc)
                  expose(nr, nc, queue);
            }
            if (safe == 0)
              state = 1;
          }
        }
      }
      snapshot(accepted);
    }
    return trace;
  }
};
