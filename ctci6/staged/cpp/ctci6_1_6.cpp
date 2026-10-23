#include <algorithm>
#include <array>
#include <string>
#include <vector>
class Solution {
 public:
  std::string Compress(const std::string& text) {
    std::string output;
    int n = static_cast<int>(text.size());
    for (int start = 0; start < n;) {
      int end = start + 1;
      while (end < n && text[end] == text[start])
        ++end;
      output.push_back(text[start]);
      output += std::to_string(end - start);
      start = end;
    }
    return static_cast<int>(output.size()) < n ? output : text;
  }
};
