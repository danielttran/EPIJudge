#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
class Solution {
 public:
  int FindMagicIndex(const std::vector<int>& values, bool distinctValues) {
    if (distinctValues) {
      int low = 0, high = static_cast<int>(values.size()) - 1;
      while (low <= high) {
        int middle = low + (high - low) / 2;
        if (values[middle] == middle)
          return middle;
        if (values[middle] > middle)
          high = middle - 1;
        else
          low = middle + 1;
      }
      return -1;
    }
    std::function<int(int, int)> search = [&](int low, int high) {
      if (low > high)
        return -1;
      int middle = low + (high - low) / 2, value = values[middle];
      if (value == middle)
        return middle;
      int left = search(low, std::min(middle - 1, value));
      return left != -1 ? left : search(std::max(middle + 1, value), high);
    };
    return search(0, static_cast<int>(values.size()) - 1);
  }
};
