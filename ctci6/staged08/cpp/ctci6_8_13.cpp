#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
class Solution {
 public:
  int MaximumBoxStackHeight(const std::vector<std::vector<int>>& boxes) {
    int n = static_cast<int>(boxes.size());
    std::vector<int> order(n), heights(n);
    for (int i = 0; i < n; ++i)
      order[i] = i;
    std::sort(order.begin(), order.end(), [&](int a, int b) { return boxes[a][0] < boxes[b][0]; });
    int best = 0;
    for (int i = 0; i < n; ++i) {
      int current = order[i];
      heights[i] = boxes[current][1];
      for (int j = 0; j < i; ++j) {
        int top = order[j];
        if (boxes[top][0] < boxes[current][0] && boxes[top][1] < boxes[current][1] &&
            boxes[top][2] < boxes[current][2])
          heights[i] = std::max(heights[i], boxes[current][1] + heights[j]);
      }
      best = std::max(best, heights[i]);
    }
    return best;
  }
};
