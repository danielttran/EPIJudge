import java.util.*;
class Solution {
  public int SwapAdjacentBits(int word) {
    return ((word & 0x55555555) << 1) | ((word & 0xaaaaaaaa) >>> 1);
  }
}
