#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
#include <unordered_set>
class Solution {
 public:
  std::vector<std::string> LargestWordRectangle(const std::vector<std::string>& words) {
    std::unordered_set<std::string> seen;
    std::vector<std::vector<std::string>> groups(6);
    int maximum = 0;
    for (const auto& word : words)
      if (seen.insert(word).second) {
        groups[word.size()].push_back(word);
        maximum = std::max(maximum, static_cast<int>(word.size()));
      }
    for (int area = maximum * maximum; area > 0; --area)
      for (int height = 1; height <= maximum; ++height) {
        if (area % height != 0)
          continue;
        int width = area / height;
        if (width > maximum || groups[width].empty() || groups[height].empty())
          continue;
        std::unordered_set<std::string> prefixes;
        for (const auto& word : groups[height])
          for (int length = 1; length <= height; ++length)
            prefixes.insert(word.substr(0, length));
        std::vector<std::string> rows;
        std::function<bool()> search = [&]() {
          if (static_cast<int>(rows.size()) == height)
            return true;
          for (const auto& word : groups[width]) {
            rows.push_back(word);
            bool valid = true;
            for (int column = 0; column < width; ++column) {
              std::string prefix;
              for (const auto& row : rows)
                prefix += row[column];
              if (!prefixes.count(prefix)) {
                valid = false;
                break;
              }
            }
            if (valid && search())
              return true;
            rows.pop_back();
          }
          return false;
        };
        if (search())
          return rows;
      }
    return {};
  }
};
