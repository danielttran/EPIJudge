import java.util.*;
class Solution {
  public int[] SumSwap(int[] first, int[] second) {
    long difference = 0;
    for (int value : first)
      difference += value;
    for (int value : second)
      difference -= value;
    if (difference % 2 != 0) {
      return new int[0];
    }
    long half = difference / 2;
    Set<Integer> contents = new HashSet<>();
    for (int value : second)
      contents.add(value);
    for (int value : first) {
      long required = (long) value - half;
      if (required >= -2147483648L && required <= 2147483647L
          && contents.contains((int) required)) {
        return new int[] {value, (int) required};
      }
    }
    return new int[0];
  }
}
