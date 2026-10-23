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
  std::string LongestComposedWord(const std::vector<std::string>& words) {
    std::unordered_set<std::string> dictionary(words.begin(), words.end());
    std::string best;
    for (const auto& word : words) {
      int n = static_cast<int>(word.size());
      std::vector<int> dp(n + 1, -1);
      dp[0] = 0;
      for (int end = 1; end <= n; ++end)
        for (int start = 0; start < end; ++start)
          if (dp[start] >= 0 && dictionary.count(word.substr(start, end - start)))
            dp[end] = std::max(dp[end], dp[start] + 1);
      if (dp[n] >= 2 && (word.size() > best.size() || (word.size() == best.size() && word < best)))
        best = word;
    }
    return best;
  }
};
