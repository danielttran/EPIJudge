import java.util.*;
class Solution {
  public int FindMagicIndex(int[] values, boolean distinctValues) {
    if (distinctValues) {
      int low = 0, high = values.length - 1;
      while (low <= high) {
        int middle = low + (high - low) / 2;
        if (values[middle] == middle)
          return middle;
        if (values[middle] > middle)
          high = middle - 1;
        else
          low = middle + 1;
      }
      return -1;
    }
    class Finder {
      int Search(int low, int high) {
        if (low > high)
          return -1;
        int middle = low + (high - low) / 2, value = values[middle];
        if (value == middle)
          return middle;
        int left = Search(low, Math.min(middle - 1, value));
        return left != -1 ? left : Search(Math.max(middle + 1, value), high);
      }
    }
    return new Finder().Search(0, values.length - 1);
  }
}
