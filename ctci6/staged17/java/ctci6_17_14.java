import java.util.*;
class Solution {
  public int[] SmallestK(int[] values, int k) {
    if (k == 0)
      return new int[0];
    var heap = new PriorityQueue<Integer>(Comparator.reverseOrder());
    for (int i = 0; i < k; ++i)
      heap.add(values[i]);
    for (int i = k; i < values.length; ++i) {
      if (values[i] < heap.peek()) {
        heap.remove();
        heap.add(values[i]);
      }
    }
    int[] result = new int[k];
    for (int i = k - 1; i >= 0; --i)
      result[i] = heap.remove();
    return result;
  }
}
