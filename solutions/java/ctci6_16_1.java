import java.util.*;
class Solution {
  public int[] SwapWithoutTemporary(int first, int second) {
    first ^= second;
    second ^= first;
    first ^= second;
    return new int[] {first, second};
  }
}
