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
  std::vector<int> WordFrequencies(const std::vector<std::string>& book,
                                   const std::vector<std::string>& queries) {
    std::unordered_map<std::string, int> counts;
    for (auto word : book) {
      for (char& c : word)
        if (c >= 'A' && c <= 'Z')
          c = static_cast<char>(c - 'A' + 'a');
      ++counts[word];
    }
    std::vector<int> result;
    result.reserve(queries.size());
    for (auto word : queries) {
      for (char& c : word)
        if (c >= 'A' && c <= 'Z')
          c = static_cast<char>(c - 'A' + 'a');
      auto found = counts.find(word);
      result.push_back(found == counts.end() ? 0 : found->second);
    }
    return result;
  }
};
