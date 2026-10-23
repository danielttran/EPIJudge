#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
class Solution {
 public:
  int KthMultiple357(int k) {
    std::vector<int> values(k + 1);
    values[0] = 1;
    int third = 0, fifth = 0, seventh = 0;
    for (int i = 1; i <= k; ++i) {
      int a = values[third] * 3, b = values[fifth] * 5, c = values[seventh] * 7,
          value = std::min(a, std::min(b, c));
      values[i] = value;
      if (value == a)
        ++third;
      if (value == b)
        ++fifth;
      if (value == c)
        ++seventh;
    }
    return values[k];
  }
};
