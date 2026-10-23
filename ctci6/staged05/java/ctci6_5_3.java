import java.util.*;
class Solution {
  public int LongestOnesAfterFlip(int word) {
    int bits = word;
    int left = 0, zeros = 0, best = 0;
    for (int right = 0; right < 32; ++right) {
      if (((bits >>> right) & 1) == 0)
        ++zeros;
      while (zeros > 1) {
        if (((bits >>> left) & 1) == 0)
          --zeros;
        ++left;
      }
      best = Math.max(best, right - left + 1);
    }
    return best;
  }
}
