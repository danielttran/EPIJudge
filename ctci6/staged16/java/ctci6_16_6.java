import java.util.*;
class Solution {
  public long SmallestDifference(int[] first, int[] second) {
    if (first.length == 0 || second.length == 0)
      return -1;
    int[] a = first.clone(), b = second.clone();
    Arrays.sort(a);
    Arrays.sort(b);
    int i = 0, j = 0;
    long best = 4294967295L;
    while (i < a.length && j < b.length) {
      long difference = (long) a[i] - b[j];
      best = Math.min(best, Math.abs(difference));
      if (difference == 0)
        return 0;
      if (difference < 0)
        ++i;
      else
        ++j;
    }
    return best;
  }
}
