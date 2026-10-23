import java.util.*;
class Solution {
  public int InsertBits(int word, int insert, int low, int high) {
    int width = high - low + 1;
    long mask = (1L << width) - 1L;
    long bits = word & 0xffffffffL, replacement = insert & 0xffffffffL;
    long result = (bits & ~(mask << low)) | ((replacement & mask) << low);
    return (int) result;
  }
}
