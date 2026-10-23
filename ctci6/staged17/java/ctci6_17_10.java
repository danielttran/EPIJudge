import java.util.*;
class Solution {
  public int[] MajorityElement(int[] values) {
    int candidate = 0, balance = 0;
    for (int value : values) {
      if (balance == 0)
        candidate = value;
      balance += value == candidate ? 1 : -1;
    }
    int count = 0;
    for (int value : values) {
      if (value == candidate)
        ++count;
    }
    if (count > values.length / 2)
      return new int[] {candidate};
    return new int[0];
  }
}
