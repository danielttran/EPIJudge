import java.util.*;
class Solution {
  public int CountCoinCombinations(int amount) {
    int[] ways = new int[amount + 1];
    ways[0] = 1;
    for (int coin : new int[] {1, 5, 10, 25}) {
      for (int value = coin; value <= amount; ++value)
        ways[value] += ways[value - coin];
    }
    return ways[amount];
  }
}
