import java.util.*;
class Solution {
  public List<List<Integer>> PowerSet(int[] values) {
    List<List<Integer>> result = new ArrayList<>();
    result.add(new ArrayList<>());
    for (int value : values) {
      int original = result.size();
      for (int i = 0; i < original; ++i) {
        var subset = new ArrayList<>(result.get(i));
        subset.add(value);
        result.add(subset);
      }
    }
    return result;
  }
}
