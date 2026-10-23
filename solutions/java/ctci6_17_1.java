import java.util.*;
class Solution {
  public int AddWithoutArithmetic(int first, int second) {
    while (second != 0) {
      int carry = (first & second) << 1;
      first ^= second;
      second = carry;
    }
    return first;
  }
}
