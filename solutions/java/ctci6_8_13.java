import java.util.*;
class Solution {
  public int MaximumBoxStackHeight(int[][] boxes) {
    int n = boxes.length;
    Integer[] order = new Integer[n];
    int[] heights = new int[n];
    for (int i = 0; i < n; ++i)
      order[i] = i;
    Arrays.sort(order, (a, b) -> Integer.compare(boxes[a][0], boxes[b][0]));
    int best = 0;
    for (int i = 0; i < n; ++i) {
      int current = order[i];
      heights[i] = boxes[current][1];
      for (int j = 0; j < i; ++j) {
        int top = order[j];
        if (boxes[top][0] < boxes[current][0] && boxes[top][1] < boxes[current][1]
            && boxes[top][2] < boxes[current][2])
          heights[i] = Math.max(heights[i], boxes[current][1] + heights[j]);
      }
      best = Math.max(best, heights[i]);
    }
    return best;
  }
}
