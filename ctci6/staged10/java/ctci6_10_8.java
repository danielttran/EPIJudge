import java.util.*;
class Solution {
  public int[] RepeatedOccurrences(int[] values) {
    byte[] bits = new byte[4000];
    int count = 0;
    for (int value : values) {
      int slot = (value - 1) >> 3, mask = 1 << ((value - 1) & 7);
      if ((bits[slot] & mask) != 0)
        ++count;
      else
        bits[slot] = (byte) (bits[slot] | mask);
    }
    int[] result = new int[count];
    Arrays.fill(bits, (byte) 0);
    int write = 0;
    for (int value : values) {
      int slot = (value - 1) >> 3, mask = 1 << ((value - 1) & 7);
      if ((bits[slot] & mask) != 0)
        result[write++] = value;
      else
        bits[slot] = (byte) (bits[slot] | mask);
    }
    return result;
  }
}
