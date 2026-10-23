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
  int AdditionOnlyArithmetic(int first, int second, const std::string& operation) {
    auto opposite = [](int value) {
      int step = value < 0 ? 1 : -1, result = 0;
      while (value != 0) {
        value += step;
        result += step;
      }
      return result;
    };
    if (operation == "subtract")
      return first + opposite(second);
    if (operation == "multiply") {
      int count = second < 0 ? opposite(second) : second,
          addend = second < 0 ? opposite(first) : first, result = 0;
      while (count > 0) {
        result += addend;
        count += -1;
      }
      return result;
    }
    int remaining = first < 0 ? opposite(first) : first,
        divisor = second < 0 ? opposite(second) : second, remove = opposite(divisor),
        step = (first < 0) == (second < 0) ? 1 : -1, quotient = 0;
    while (remaining + remove >= 0) {
      remaining += remove;
      quotient += step;
    }
    return quotient;
  }
};
