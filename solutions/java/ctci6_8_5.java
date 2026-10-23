import java.util.*;
class Solution {
  public int RecursiveMultiply(int first, int second) {
    int smaller = Math.min(first, second), larger = Math.max(first, second);
    if (smaller == 0)
      return 0;
    int half = RecursiveMultiply(smaller >> 1, larger);
    return half + half + ((smaller & 1) != 0 ? larger : 0);
  }
}
