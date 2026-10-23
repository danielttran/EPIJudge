import java.util.*;
class Solution {
  public int MaximumMassageMinutes(int[] appointments) {
    int oneBack = 0, twoBack = 0;
    for (int duration : appointments) {
      int current = Math.max(oneBack, duration + twoBack);
      twoBack = oneBack;
      oneBack = current;
    }
    return oneBack;
  }
}
