#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
class Solution {
 public:
  std::vector<int> SmallestK(const std::vector<int>& values, int k) {
    if (k == 0)
      return {};
    std::vector<int> heap(values.begin(), values.begin() + k);
    std::make_heap(heap.begin(), heap.end());
    for (int i = k; i < static_cast<int>(values.size()); ++i) {
      if (values[i] < heap.front()) {
        std::pop_heap(heap.begin(), heap.end());
        heap.back() = values[i];
        std::push_heap(heap.begin(), heap.end());
      }
    }
    std::sort_heap(heap.begin(), heap.end());
    return heap;
  }
};
