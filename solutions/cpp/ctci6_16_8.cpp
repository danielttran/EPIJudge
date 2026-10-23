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
  std::string EnglishInteger(int value) {
    if (value == 0)
      return "Zero";
    const std::vector<std::string> small = {"Zero",    "One",       "Two",      "Three",
                                            "Four",    "Five",      "Six",      "Seven",
                                            "Eight",   "Nine",      "Ten",      "Eleven",
                                            "Twelve",  "Thirteen",  "Fourteen", "Fifteen",
                                            "Sixteen", "Seventeen", "Eighteen", "Nineteen"},
                                   tens = {"",      "",      "Twenty",  "Thirty", "Forty",
                                           "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"},
                                   scales = {"", "Thousand", "Million", "Billion"};
    long long magnitude = value;
    if (magnitude < 0)
      magnitude = -magnitude;
    std::vector<std::string> groups;
    int scale = 0;
    while (magnitude > 0) {
      int chunk = static_cast<int>(magnitude % 1000);
      if (chunk != 0) {
        std::vector<std::string> words;
        if (chunk >= 100) {
          words.push_back(small[chunk / 100]);
          words.push_back("Hundred");
          chunk %= 100;
        }
        if (chunk >= 20) {
          words.push_back(tens[chunk / 10]);
          chunk %= 10;
        }
        if (chunk != 0)
          words.push_back(small[chunk]);
        if (scale != 0)
          words.push_back(scales[scale]);
        std::string part;
        for (const auto& word : words) {
          if (!part.empty())
            part += " ";
          part += word;
        }
        groups.push_back(part);
      }
      magnitude /= 1000;
      ++scale;
    }
    std::string result = value < 0 ? "Negative " : "";
    for (auto it = groups.rbegin(); it != groups.rend(); ++it) {
      if (it != groups.rbegin())
        result += " ";
      result += *it;
    }
    return result;
  }
};
