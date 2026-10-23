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
  int CountFactorialZeros(int n) {
    int count = 0;
    while (n != 0) {
      n /= 5;
      count += n;
    }
    return count;
  }
};
