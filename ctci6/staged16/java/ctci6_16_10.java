import java.util.*;
class Solution {
  public int MostPopulatedYear(int[][] people) {
    int[] changes = new int[102];
    for (int[] person : people) {
      ++changes[person[0] - 1900];
      --changes[person[1] - 1900 + 1];
    }
    int alive = 0, best = 0, answer = 1900;
    for (int offset = 0; offset < 101; ++offset) {
      alive += changes[offset];
      if (alive > best) {
        best = alive;
        answer = 1900 + offset;
      }
    }
    return answer;
  }
}
