import java.util.*;
class Solution {
  public int[] ArrangePeaksValleys(int[] values) {
    for (int i = 1; i < values.length; i += 2) {
      int best = i;
      if (values[i - 1] > values[best])
        best = i - 1;
      if (i + 1 < values.length && values[i + 1] > values[best])
        best = i + 1;
      int temporary = values[i];
      values[i] = values[best];
      values[best] = temporary;
    }
    return values;
  }
}
