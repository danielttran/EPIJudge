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
  int MostPopulatedYear(const std::vector<std::vector<int>>& people) {
    int changes[102] = {};
    for (const auto& person : people) {
      ++changes[person[0] - 1900];
      --changes[person[1] - 1900 + 1];
    }
    int alive = 0, best = 0, answer = 1900;
    for (int offset = 0; offset < 101; ++offset) {
      alive += changes[offset];
      if (alive > best) {
        best = alive;
        answer = 1900 + offset;
      }
    }
    return answer;
  }
};
