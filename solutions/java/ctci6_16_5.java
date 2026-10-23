import java.util.*;
class Solution {
  public int CountFactorialZeros(int n) {
    int count = 0;
    while (n != 0) {
      n /= 5;
      count += n;
    }
    return count;
  }
}
