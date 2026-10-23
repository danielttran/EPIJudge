#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
class Solution {
 public:
  int RecursiveMultiply(int first, int second) {
    int smaller = std::min(first, second), larger = std::max(first, second);
    if (smaller == 0)
      return 0;
    int half = RecursiveMultiply(smaller >> 1, larger);
    return half + half + ((smaller & 1) != 0 ? larger : 0);
  }
};
