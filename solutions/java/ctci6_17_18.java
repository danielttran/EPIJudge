import java.util.*;
class Solution {
  public int[] ShortestCoveringRange(int[] big, int[] small) {
    if (small.length == 0)
      return new int[] {-1, -1};
    Map<Integer, Integer> counts = new HashMap<>();
    for (int value : small)
      counts.put(value, 0);
    int missing = small.length, left = 0, start = -1, end = -1;
    for (int right = 0; right < big.length; ++right) {
      int value = big[right];
      if (counts.containsKey(value)) {
        if (counts.get(value) == 0)
          --missing;
        counts.put(value, counts.get(value) + 1);
      }
      while (missing == 0) {
        if (start == -1 || right - left < end - start) {
          start = left;
          end = right;
        }
        int removed = big[left];
        if (counts.containsKey(removed)) {
          counts.put(removed, counts.get(removed) - 1);
          if (counts.get(removed) == 0)
            ++missing;
        }
        ++left;
      }
    }
    return new int[] {start, end};
  }
}
