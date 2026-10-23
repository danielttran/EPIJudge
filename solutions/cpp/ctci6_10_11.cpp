#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
class Solution {
 public:
  std::vector<int> ArrangePeaksValleys(std::vector<int>& values) {
    for (int i = 1; i < static_cast<int>(values.size()); i += 2) {
      int best = i;
      if (values[i - 1] > values[best])
        best = i - 1;
      if (i + 1 < static_cast<int>(values.size()) && values[i + 1] > values[best])
        best = i + 1;
      std::swap(values[i], values[best]);
    }
    return values;
  }
};
