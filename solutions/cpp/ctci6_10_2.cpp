#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
class Solution {
 public:
  std::vector<std::string> GroupAnagrams(std::vector<std::string>& words) {
    std::vector<std::pair<std::string, std::string>> decorated;
    decorated.reserve(words.size());
    for (const auto& word : words) {
      auto key = word;
      std::sort(key.begin(), key.end());
      decorated.emplace_back(key, word);
    }
    std::sort(decorated.begin(), decorated.end());
    for (size_t i = 0; i < words.size(); ++i)
      words[i] = decorated[i].second;
    return words;
  }
};
