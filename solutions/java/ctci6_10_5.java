import java.util.*;
class Solution {
  public int SparseSearch(String[] words, String target) {
    if (target.isEmpty())
      return -1;
    int low = 0, high = words.length - 1;
    while (low <= high) {
      int middle = low + (high - low) / 2;
      if (words[middle].isEmpty()) {
        int left = middle - 1, right = middle + 1;
        while (true) {
          if (left < low && right > high)
            return -1;
          if (right <= high && !(words[right].isEmpty())) {
            middle = right;
            break;
          }
          if (left >= low && !(words[left].isEmpty())) {
            middle = left;
            break;
          }
          --left;
          ++right;
        }
      }
      int comparison = words[middle].compareTo(target);
      if (comparison == 0)
        return middle;
      if (comparison < 0)
        low = middle + 1;
      else
        high = middle - 1;
    }
    return -1;
  }
}
