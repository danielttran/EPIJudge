import java.util.*;
class Solution {
  public int[][] PairsWithSum(int[] values, int target) {
    int[] ordered = values.clone();
    Arrays.sort(ordered);
    List<int[]> result = new ArrayList<>();
    int left = 0, right = ordered.length - 1;
    while (left < right) {
      long total = (long) ordered[left] + ordered[right];
      if (total == target) {
        result.add(new int[] {ordered[left], ordered[right]});
        ++left;
        --right;
      } else if (total < target)
        ++left;
      else
        --right;
    }
    return result.toArray(new int[0][]);
  }
}
