#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
class Solution {
 public:
  std::vector<std::string> PermutationsDistinct(const std::string& text) {
    std::string chars = text;
    std::vector<std::string> result;
    std::function<void(int)> visit = [&](int depth) {
      if (depth == static_cast<int>(chars.size())) {
        result.push_back(chars);
        return;
      }
      for (int i = depth; i < static_cast<int>(chars.size()); ++i) {
        char temporary = chars[depth];
        chars[depth] = chars[i];
        chars[i] = temporary;
        visit(depth + 1);
        temporary = chars[depth];
        chars[depth] = chars[i];
        chars[i] = temporary;
      }
    };
    visit(0);
    return result;
  }
};
