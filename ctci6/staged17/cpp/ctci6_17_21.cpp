#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
class Solution {
 public:
  int HistogramWaterVolume(const std::vector<int>& heights) {
    int left = 0, right = static_cast<int>(heights.size()) - 1, leftMax = 0, rightMax = 0,
        volume = 0;
    while (left <= right) {
      if (leftMax <= rightMax) {
        leftMax = std::max(leftMax, heights[left]);
        volume += leftMax - heights[left];
        ++left;
      } else {
        rightMax = std::max(rightMax, heights[right]);
        volume += rightMax - heights[right];
        --right;
      }
    }
    return volume;
  }
};
