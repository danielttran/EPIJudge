import java.util.*;
class Solution {
  public int[] SameWeightNeighbors(int number) {
    java.util.function.LongUnaryOperator successor = value -> {
      if (value == 0)
        return -1L;
      long lowest = value & -value, raised = value + lowest;
      if (raised > 2147483647)
        return -1L;
      return raised | (((raised ^ value) / lowest) >> 2);
    };
    long larger = successor.applyAsLong(number),
         reverse = successor.applyAsLong(2147483647 ^ number),
         smaller = reverse == -1 ? -1 : (2147483647 ^ reverse);
    return new int[] {(int) (smaller), (int) (larger)};
  }
}
