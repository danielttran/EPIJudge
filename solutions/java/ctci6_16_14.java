import java.util.*;
class Solution {
  public int[] BestLine(int[][] points) {
    if (points.length == 0)
      return new int[0];
    class MathHelper {
      int gcd(int a, int b) {
        while (b != 0) {
          int next = a % b;
          a = b;
          b = next;
        }
        return a;
      }
    }
    var math = new MathHelper();
    int[] best = {1, 0, -points[0][0]};
    int bestCount = 0;
    for (int anchor = 0; anchor < points.length; ++anchor) {
      Map<Integer, Integer> groups = new HashMap<>();
      int duplicates = 0, x = points[anchor][0], y = points[anchor][1];
      for (int other = anchor + 1; other < points.length; ++other) {
        int dx = points[other][0] - x, dy = points[other][1] - y;
        if (dx == 0 && dy == 0) {
          ++duplicates;
          continue;
        }
        int divisor = math.gcd(Math.abs(dx), Math.abs(dy));
        dx /= divisor;
        dy /= divisor;
        if (dx < 0 || (dx == 0 && dy < 0)) {
          dx = -dx;
          dy = -dy;
        }
        int key = (dy + 2000) * 4001 + dx;
        groups.put(key, groups.getOrDefault(key, 0) + 1);
      }
      for (var entry : groups.entrySet())
        if (entry.getValue() + duplicates + 1 > bestCount) {
          bestCount = entry.getValue() + duplicates + 1;
          int a = entry.getKey() / 4001 - 2000, b = -(entry.getKey() % 4001), c = -a * x - b * y;
          if (a < 0 || (a == 0 && b < 0)) {
            a = -a;
            b = -b;
            c = -c;
          }
          best = new int[] {a, b, c};
        }
    }
    return best;
  }
}
