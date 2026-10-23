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
  std::vector<int> DivingBoardLengths(int planks, int shorter, int longer) {
    if (shorter == longer)
      return {planks * shorter};
    std::vector<int> result;
    result.reserve(planks + 1);
    for (int count = 0; count <= planks; ++count)
      result.push_back(planks * shorter + count * (longer - shorter));
    return result;
  }
};
