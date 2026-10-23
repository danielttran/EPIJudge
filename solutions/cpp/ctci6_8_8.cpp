#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
class Solution {
 public:
  std::vector<std::string> PermutationsWithDuplicates(const std::string& text) {
    std::array<int, 26> counts{};
    for (char c : text)
      ++counts[c - 'a'];
    std::string buffer(text.size(), ' ');
    std::vector<std::string> result;
    std::function<void(int)> visit = [&](int depth) {
      if (depth == static_cast<int>(buffer.size())) {
        result.push_back(buffer);
        return;
      }
      for (int letter = 0; letter < 26; ++letter) {
        if (counts[letter] > 0) {
          --counts[letter];
          buffer[depth] = static_cast<char>('a' + letter);
          visit(depth + 1);
          ++counts[letter];
        }
      }
    };
    visit(0);
    return result;
  }
};
