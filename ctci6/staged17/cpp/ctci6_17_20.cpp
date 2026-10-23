#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
#include <queue>
class Solution {
 public:
  std::vector<double> ContinuousMedians(const std::vector<int>& values) {
    std::priority_queue<int> lower;
    std::priority_queue<int, std::vector<int>, std::greater<int>> upper;
    std::vector<double> medians;
    medians.reserve(values.size());
    for (int value : values) {
      if (lower.empty() || value <= lower.top())
        lower.push(value);
      else
        upper.push(value);
      if (lower.size() > upper.size() + 1) {
        upper.push(lower.top());
        lower.pop();
      } else if (upper.size() > lower.size()) {
        lower.push(upper.top());
        upper.pop();
      }
      medians.push_back(lower.size() > upper.size()
                            ? lower.top()
                            : (static_cast<double>(lower.top()) + upper.top()) / 2.0);
    }
    return medians;
  }
};
