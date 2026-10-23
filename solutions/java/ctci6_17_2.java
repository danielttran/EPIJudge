import java.util.*;
class RandomSource { static java.util.function.IntBinaryOperator Draw=(lower,upper)->{throw new IllegalStateException("Provided by the judge");}; public static int GetRandom(int lower,int upper){return Draw.applyAsInt(lower,upper);} }
class Solution {
  public void Shuffle(int[] values) {
    for (int index = values.length - 1; index > 0; --index) {
      int other = RandomSource.GetRandom(0, index), saved = values[index];
      values[index] = values[other];
      values[other] = saved;
    }
  }
}
