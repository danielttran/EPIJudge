#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
class Solution {
 public:
  std::vector<std::vector<int>> TrueNameFrequencies(const std::vector<std::string>& names,
                                                    const std::vector<int>& frequencies,
                                                    const std::vector<std::vector<int>>& synonyms) {
    int n = static_cast<int>(names.size());
    std::vector<std::vector<int>> adjacent(n), result;
    for (const auto& edge : synonyms) {
      adjacent[edge[0]].push_back(edge[1]);
      adjacent[edge[1]].push_back(edge[0]);
    }
    std::vector<bool> visited(n, false);
    for (int start = 0; start < n; ++start) {
      if (visited[start])
        continue;
      visited[start] = true;
      std::vector<int> queue{start};
      int total = 0;
      for (size_t head = 0; head < queue.size(); ++head) {
        int name = queue[head];
        total += frequencies[name];
        for (int other : adjacent[name])
          if (!visited[other]) {
            visited[other] = true;
            queue.push_back(other);
          }
      }
      result.push_back({start, total});
    }
    return result;
  }
};
