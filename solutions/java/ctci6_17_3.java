import java.util.*;
class RandomSource { static java.util.function.IntBinaryOperator Draw=(lower,upper)->{throw new IllegalStateException("Provided by the judge");}; public static int GetRandom(int lower,int upper){return Draw.applyAsInt(lower,upper);} }
class Solution {
  public int[] RandomSubset(int[] values, int count) {
    int[] reservoir = Arrays.copyOf(values, count);
    if (count == 0)
      return reservoir;
    for (int index = count; index < values.length; ++index) {
      int slot = RandomSource.GetRandom(0, index);
      if (slot < count)
        reservoir[slot] = values[index];
    }
    return reservoir;
  }
}
