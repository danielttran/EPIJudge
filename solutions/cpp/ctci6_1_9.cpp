#include <algorithm>
#include <array>
#include <string>
#include <vector>
class Solution {
 public:
  bool IsRotation(const std::string& first, const std::string& second) {
    if (static_cast<int>(first.size()) == 0 ||
        static_cast<int>(first.size()) != static_cast<int>(second.size()))
      return false;
    return (first + first).find(second) != std::string::npos;
  }
};
