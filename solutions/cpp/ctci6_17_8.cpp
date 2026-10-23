#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
class Solution {
 public:
  std::vector<int> CircusTower(const std::vector<std::vector<int>>& people) {
    int n = static_cast<int>(people.size());
    if (n == 0)
      return {};
    std::vector<int> order(n), length(n, 1), previous(n, -1);
    for (int i = 0; i < n; ++i)
      order[i] = i;
    std::sort(order.begin(), order.end(), [&](int a, int b) {
      if (people[a][0] != people[b][0])
        return people[a][0] < people[b][0];
      if (people[a][1] != people[b][1])
        return people[a][1] < people[b][1];
      return a < b;
    });
    int best = 0;
    for (int i = 0; i < n; ++i) {
      for (int j = 0; j < i; ++j)
        if (people[order[j]][0] < people[order[i]][0] &&
            people[order[j]][1] < people[order[i]][1] && length[j] + 1 > length[i]) {
          length[i] = length[j] + 1;
          previous[i] = j;
        }
      if (length[i] > length[best])
        best = i;
    }
    std::vector<int> result;
    for (int at = best; at != -1; at = previous[at])
      result.push_back(order[at]);
    std::reverse(result.begin(), result.end());
    return result;
  }
};
