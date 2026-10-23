import java.util.*;
class Solution {
  public int CountBitChanges(int first, int second) {
    int difference = first ^ second, count = 0;
    while (difference != 0) {
      difference &= difference - 1;
      ++count;
    }
    return count;
  }
}
