import java.util.*;
class Solution {
  public int MaximumWithoutComparison(int first, int second) {
    int negativeFirst = first >>> 31, negativeSecond = second >>> 31,
        negativeDifference = (first - second) >>> 31;
    int different = negativeFirst ^ negativeSecond,
        chooseFirst = different * (negativeFirst ^ 1) + (different ^ 1) * (negativeDifference ^ 1),
        mask = -chooseFirst;
    return (first & mask) | (second & ~mask);
  }
}
