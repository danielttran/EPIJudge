#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
class Solution {
 public:
  std::vector<std::string> GenerateParentheses(int pairs) {
    std::string buffer(2 * pairs, ' ');
    std::vector<std::string> result;
    std::function<void(int, int)> visit = [&](int opened, int closed) {
      int position = opened + closed;
      if (position == static_cast<int>(buffer.size())) {
        result.push_back(buffer);
        return;
      }
      if (opened < pairs) {
        buffer[position] = '(';
        visit(opened + 1, closed);
      }
      if (closed < opened) {
        buffer[position] = ')';
        visit(opened, closed + 1);
      }
    };
    visit(0, 0);
    return result;
  }
};
