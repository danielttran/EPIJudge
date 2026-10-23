import java.util.*;
class Solution {
  public int HistogramWaterVolume(int[] heights) {
    int left = 0, right = heights.length - 1, leftMax = 0, rightMax = 0, volume = 0;
    while (left <= right) {
      if (leftMax <= rightMax) {
        leftMax = Math.max(leftMax, heights[left]);
        volume += leftMax - heights[left];
        ++left;
      } else {
        rightMax = Math.max(rightMax, heights[right]);
        volume += rightMax - heights[right];
        --right;
      }
    }
    return volume;
  }
}
