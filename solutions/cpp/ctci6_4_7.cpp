#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
class Solution {
 public:
  std::vector<int> BuildOrder(int projectCount, const std::vector<std::vector<int>>& dependencies) {
    std::vector<std::vector<int>> adjacent(projectCount);
    std::vector<int> indegree(projectCount, 0), order;
    for (const auto& edge : dependencies) {
      adjacent[edge[0]].push_back(edge[1]);
      ++indegree[edge[1]];
    }
    for (int i = 0; i < projectCount; ++i)
      if (indegree[i] == 0)
        order.push_back(i);
    for (size_t head = 0; head < order.size(); ++head)
      for (int dependent : adjacent[order[head]]) {
        --indegree[dependent];
        if (indegree[dependent] == 0)
          order.push_back(dependent);
      }
    if (order.size() != static_cast<size_t>(projectCount))
      return {};
    return order;
  }
};
