#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
class Solution {
 public:
  std::vector<int> SwapWithoutTemporary(int first, int second) {
    first ^= second;
    second ^= first;
    first ^= second;
    return {first, second};
  }
};
