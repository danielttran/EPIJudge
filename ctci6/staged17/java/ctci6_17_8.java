import java.util.*;
class Solution {
  public int[] CircusTower(int[][] people) {
    int n = people.length;
    if (n == 0)
      return new int[0];
    Integer[] order = new Integer[n];
    int[] length = new int[n], previous = new int[n];
    for (int i = 0; i < n; ++i)
      order[i] = i;
    Arrays.sort(order, (a, b) -> {
      int height = Integer.compare(people[a][0], people[b][0]);
      if (height != 0)
        return height;
      int weight = Integer.compare(people[a][1], people[b][1]);
      return weight != 0 ? weight : Integer.compare(a, b);
    });
    Arrays.fill(length, 1);
    Arrays.fill(previous, -1);
    int best = 0;
    for (int i = 0; i < n; ++i) {
      for (int j = 0; j < i; ++j)
        if (people[order[j]][0] < people[order[i]][0] && people[order[j]][1] < people[order[i]][1]
            && length[j] + 1 > length[i]) {
          length[i] = length[j] + 1;
          previous[i] = j;
        }
      if (length[i] > length[best])
        best = i;
    }
    int[] result = new int[length[best]];
    for (int at = result.length - 1; at >= 0; --at) {
      result[at] = order[best];
      best = previous[best];
    }
    return result;
  }
}
