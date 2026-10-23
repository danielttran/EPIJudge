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
  std::vector<std::vector<int>> SolveJigsaw(int size, const std::vector<std::vector<int>>& pieces) {
    int count = static_cast<int>(pieces.size());
    std::vector<std::vector<int>> placed(count, std::vector<int>(2));
    std::vector<bool> used(count, false);
    auto edge = [&](int index, int turn, int side) { return pieces[index][(side - turn + 4) % 4]; };
    std::function<bool(int)> search = [&](int position) {
      if (position == count)
        return true;
      int row = position / size, column = position % size;
      for (int index = 0; index < count; ++index) {
        if (used[index])
          continue;
        for (int turn = 0; turn < 4; ++turn) {
          int values[4];
          bool bounds[4] = {row == 0, column == size - 1, row == size - 1, column == 0},
               fits = true;
          for (int side = 0; side < 4; ++side) {
            values[side] = edge(index, turn, side);
            if ((values[side] == 0) != bounds[side])
              fits = false;
          }
          if (!fits)
            continue;
          if (row && values[0] != -edge(placed[position - size][0], placed[position - size][1], 2))
            continue;
          if (column && values[3] != -edge(placed[position - 1][0], placed[position - 1][1], 1))
            continue;
          used[index] = true;
          placed[position] = {index, turn};
          if (search(position + 1))
            return true;
          used[index] = false;
        }
      }
      return false;
    };
    return search(0) ? placed : std::vector<std::vector<int>>{};
  }
};
