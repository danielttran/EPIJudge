import java.util.*;
class Solution {
  public int[] ShortestSortWindow(int[] values) {
    int n = values.length;
    if (n == 0)
      return new int[] {-1, -1};
    int right = -1, maximum = values[0];
    for (int i = 0; i < n; ++i) {
      if (values[i] < maximum)
        right = i;
      maximum = Math.max(maximum, values[i]);
    }
    if (right == -1)
      return new int[] {-1, -1};
    int left = -1, minimum = values[n - 1];
    for (int i = n - 1; i >= 0; --i) {
      if (values[i] > minimum)
        left = i;
      minimum = Math.min(minimum, values[i]);
    }
    return new int[] {left, right};
  }
}
