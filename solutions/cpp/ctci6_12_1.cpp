#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
#include <fstream>
#include <deque>
#include <filesystem>
class Solution {
 public:
  std::vector<std::string> LastKLines(const std::string& filePath, int k) {
    std::ifstream input(filePath);
    if (!input)
      throw std::runtime_error("Could not open input file");
    std::deque<std::string> suffix;
    std::string line;
    while (std::getline(input, line)) {
      suffix.push_back(line);
      if (suffix.size() > static_cast<std::size_t>(k))
        suffix.pop_front();
    }
    if (input.bad())
      throw std::runtime_error("Could not read input file");
    return std::vector<std::string>(suffix.begin(), suffix.end());
  }
};
