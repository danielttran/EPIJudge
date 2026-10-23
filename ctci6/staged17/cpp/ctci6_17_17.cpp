#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
class Solution {
 public:
  std::vector<std::vector<int>> MultiSearch(const std::string& text,
                                            const std::vector<std::string>& patterns) {
    std::vector<std::vector<int>> result;
    for (const auto& pattern : patterns) {
      std::vector<int> positions;
      int limit = static_cast<int>(text.size()) - static_cast<int>(pattern.size());
      for (int start = 0; start <= limit; ++start)
        if (text.compare(start, pattern.size(), pattern) == 0)
          positions.push_back(start);
      result.push_back(std::move(positions));
    }
    return result;
  }
};
