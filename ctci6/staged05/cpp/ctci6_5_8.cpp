#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
class Solution {
 public:
  void DrawHorizontalLine(std::vector<std::uint8_t>& screen, int width, int x1, int x2, int y) {
    int first = x1 / 8, last = x2 / 8, row = y * (width / 8);
    for (int cell = first; cell <= last; ++cell) {
      int start = cell == first ? x1 % 8 : 0, end = cell == last ? x2 % 8 : 7,
          mask = (255 >> start) & ((255 << (7 - end)) & 255);
      screen[row + cell] = static_cast<std::uint8_t>(screen[row + cell] | mask);
    }
  }
};
