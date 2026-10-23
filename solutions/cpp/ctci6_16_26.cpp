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
  double Calculate(const std::string& expression) {
    double total = 0, term = 0;
    char op = '+';
    size_t index = 0;
    while (index < expression.size()) {
      int number = 0;
      while (index < expression.size() && expression[index] >= '0' && expression[index] <= '9') {
        number = number * 10 + expression[index] - '0';
        ++index;
      }
      if (op == '+') {
        total += term;
        term = number;
      } else if (op == '-') {
        total += term;
        term = -number;
      } else if (op == '*')
        term *= number;
      else
        term /= number;
      if (index < expression.size())
        op = expression[index++];
    }
    return total + term;
  }
};
