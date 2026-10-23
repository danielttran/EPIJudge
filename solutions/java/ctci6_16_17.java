import java.util.*;
class Solution {
  public int MaximumContiguousSum(int[] values) {
    int running = 0, best = 0;
    for (int value : values) {
      running = Math.max(0, running + value);
      best = Math.max(best, running);
    }
    return best;
  }
}
