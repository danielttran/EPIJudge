import java.util.*;
class Solution {
  public int[] MissingTwo(int[] values) {
    int n = values.length + 2, combined = 0;
    for (int value = 1; value <= n; ++value)
      combined ^= value;
    for (int value : values)
      combined ^= value;
    int bit = combined & -combined, first = 0, second = 0;
    for (int value = 1; value <= n; ++value) {
      if ((value & bit) != 0)
        first ^= value;
      else
        second ^= value;
    }
    for (int value : values) {
      if ((value & bit) != 0)
        first ^= value;
      else
        second ^= value;
    }
    return new int[] {Math.min(first, second), Math.max(first, second)};
  }
}
