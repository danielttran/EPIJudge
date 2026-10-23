#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
class Solution {
 public:
  std::vector<int> SearchSortedMatrix(const std::vector<std::vector<int>>& matrix, int target) {
    int rows = static_cast<int>(matrix.size()),
        columns = rows == 0 ? 0 : static_cast<int>(matrix[0].size()), row = 0, column = columns - 1;
    while (row < rows && column >= 0) {
      int value = matrix[row][column];
      if (value == target)
        return {row, column};
      if (value > target)
        --column;
      else
        ++row;
    }
    return {-1, -1};
  }
};
