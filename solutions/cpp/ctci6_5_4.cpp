#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
class Solution {
 public:
  std::vector<int> SameWeightNeighbors(int number) {
    auto successor = [](long long value) -> long long {
      if (value == 0)
        return -1LL;
      long long lowest = value & -value, raised = value + lowest;
      if (raised > 2147483647)
        return -1LL;
      return raised | (((raised ^ value) / lowest) >> 2);
    };
    long long larger = successor(number), reverse = successor(2147483647 ^ number),
              smaller = reverse == -1 ? -1 : (2147483647 ^ reverse);
    return {static_cast<int>(smaller), static_cast<int>(larger)};
  }
};
