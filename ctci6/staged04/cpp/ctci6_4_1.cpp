#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
class Solution {
 public:
  bool HasDirectedRoute(int nodeCount, const std::vector<std::vector<int>>& edges, int start,
                        int target) {
    if (start == target)
      return true;
    std::vector<std::vector<int>> adjacent(nodeCount);
    for (const auto& edge : edges)
      adjacent[edge[0]].push_back(edge[1]);
    std::vector<bool> visited(nodeCount, false);
    std::vector<int> queue{start};
    visited[start] = true;
    for (size_t head = 0; head < queue.size(); ++head)
      for (int neighbor : adjacent[queue[head]])
        if (!visited[neighbor]) {
          if (neighbor == target)
            return true;
          visited[neighbor] = true;
          queue.push_back(neighbor);
        }
    return false;
  }
};
