#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
class Solution {
 public:
  std::vector<int> LongestLettersDigits(const std::string& text) {
    int n = static_cast<int>(text.size());
    std::vector<int> first(2 * n + 1, -2);
    first[n] = -1;
    int balance = 0, best = 0, start = -1, end = -1;
    for (int i = 0; i < n; ++i) {
      balance += (text[i] >= '0' && text[i] <= '9') ? -1 : 1;
      int slot = balance + n;
      if (first[slot] == -2)
        first[slot] = i;
      else if (i - first[slot] > best) {
        best = i - first[slot];
        start = first[slot] + 1;
        end = i;
      }
    }
    return {start, end};
  }
};
