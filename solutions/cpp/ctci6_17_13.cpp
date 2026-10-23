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
  std::vector<std::string> ReSpace(const std::string& text,
                                   const std::vector<std::string>& dictionary) {
    std::unordered_set<std::string> words(dictionary.begin(), dictionary.end());
    int maximum = 0;
    for (const auto& word : words)
      maximum = std::max(maximum, static_cast<int>(word.size()));
    int n = static_cast<int>(text.size());
    std::vector<int> cost(n + 1, 0), previous(n + 1, 0);
    for (int end = 1; end <= n; ++end) {
      cost[end] = cost[end - 1] + 1;
      previous[end] = end - 1;
      for (int length = 1; length <= maximum && length <= end; ++length) {
        int start = end - length;
        if (words.count(text.substr(start, length)) && cost[start] < cost[end]) {
          cost[end] = cost[start];
          previous[end] = start;
        }
      }
    }
    std::vector<std::string> result;
    for (int end = n; end > 0; end = previous[end])
      result.push_back(text.substr(previous[end], end - previous[end]));
    std::reverse(result.begin(), result.end());
    return result;
  }
};
