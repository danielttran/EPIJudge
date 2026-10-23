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
  std::vector<std::string> EncodeXml(const std::vector<std::string>& elementNames,
                                     const std::vector<std::string>& elementTexts,
                                     const std::vector<std::vector<int>>& children,
                                     const std::vector<int>& attributeOwners,
                                     const std::vector<std::string>& attributeNames,
                                     const std::vector<std::string>& attributeValues,
                                     const std::vector<std::string>& codeNames,
                                     const std::vector<int>& codes) {
    std::vector<std::string> result;
    if (elementNames.empty())
      return result;
    std::unordered_map<std::string, std::string> lookup;
    for (size_t i = 0; i < codeNames.size(); ++i)
      lookup[codeNames[i]] = std::to_string(codes[i]);
    std::vector<std::vector<size_t>> attributes(elementNames.size());
    for (size_t i = 0; i < attributeOwners.size(); ++i)
      attributes[attributeOwners[i]].push_back(i);
    std::vector<std::pair<int, bool>> events{{0, false}};
    while (!events.empty()) {
      auto frame = events.back();
      events.pop_back();
      int node = frame.first;
      if (frame.second) {
        result.push_back("0");
        continue;
      }
      result.push_back(lookup.at(elementNames[node]));
      for (size_t attribute : attributes[node]) {
        result.push_back(lookup.at(attributeNames[attribute]));
        result.push_back(attributeValues[attribute]);
      }
      result.push_back("0");
      events.emplace_back(node, true);
      if (!elementTexts[node].empty())
        result.push_back(elementTexts[node]);
      else
        for (auto it = children[node].rbegin(); it != children[node].rend(); ++it)
          events.emplace_back(*it, false);
    }
    return result;
  }
};
