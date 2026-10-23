import java.util.*;
class Solution {
  public int[] LongestLettersDigits(String text) {
    int n = text.length();
    int[] first = new int[2 * n + 1];
    Arrays.fill(first, -2);
    first[n] = -1;
    int balance = 0, best = 0, start = -1, end = -1;
    for (int i = 0; i < n; ++i) {
      balance += (text.charAt(i) >= '0' && text.charAt(i) <= '9') ? -1 : 1;
      int slot = balance + n;
      if (first[slot] == -2)
        first[slot] = i;
      else if (i - first[slot] > best) {
        best = i - first[slot];
        start = first[slot] + 1;
        end = i;
      }
    }
    return new int[] {start, end};
  }
}
