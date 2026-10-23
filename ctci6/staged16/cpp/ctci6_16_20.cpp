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
  std::vector<std::string> T9Words(const std::string& digits,
                                   const std::vector<std::string>& dictionary) {
    const std::string mapping = "22233344455566677778889999";
    std::vector<std::string> result;
    for (const auto& word : dictionary) {
      if (word.size() != digits.size())
        continue;
      bool valid = true;
      for (size_t i = 0; i < word.size(); ++i)
        if (mapping[word[i] - 'a'] != digits[i]) {
          valid = false;
          break;
        }
      if (valid)
        result.push_back(word);
    }
    return result;
  }
};
