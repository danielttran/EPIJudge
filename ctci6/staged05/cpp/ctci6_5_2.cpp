#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
class Solution {
 public:
  std::string BinaryFraction(double number) {
    if (number <= 0 || number >= 1)
      return "ERROR";
    std::string result = ".";
    for (int i = 0; i < 31; ++i) {
      number *= 2;
      bool bit = number >= 1;
      result.push_back(bit ? '1' : '0');
      if (bit)
        --number;
      if (number == 0)
        return result;
    }
    return "ERROR";
  }
};
