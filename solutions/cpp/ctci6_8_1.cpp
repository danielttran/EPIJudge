#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
class Solution {
 public:
  int CountTripleSteps(int steps) {
    if (steps < 0)
      return 0;
    int previous = 1, older = 0, oldest = 0;
    for (int i = 0; i < steps; ++i) {
      int current = previous + older + oldest;
      oldest = older;
      older = previous;
      previous = current;
    }
    return previous;
  }
};
