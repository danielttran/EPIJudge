import java.util.*;
abstract class FairCoinSource {public abstract boolean Next();}
class Solution {
  public int[] RandomSubset(int[] values, FairCoinSource coins) {
    return Arrays.stream(values).filter(value -> coins.Next()).toArray();
  }
}
