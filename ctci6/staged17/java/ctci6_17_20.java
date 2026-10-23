import java.util.*;
class Solution {
  public double[] ContinuousMedians(int[] values) {
    var lower = new PriorityQueue<Integer>(Comparator.reverseOrder());
    var upper = new PriorityQueue<Integer>();
    double[] medians = new double[values.length];
    for (int i = 0; i < values.length; ++i) {
      int value = values[i];
      if (lower.isEmpty() || value <= lower.peek())
        lower.add(value);
      else
        upper.add(value);
      if (lower.size() > upper.size() + 1)
        upper.add(lower.remove());
      else if (upper.size() > lower.size())
        lower.add(upper.remove());
      medians[i] =
          lower.size() > upper.size() ? lower.peek() : ((double) lower.peek() + upper.peek()) / 2.0;
    }
    return medians;
  }
}
