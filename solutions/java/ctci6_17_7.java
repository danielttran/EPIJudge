import java.util.*;
class Solution {
  public int[][] TrueNameFrequencies(String[] names, int[] frequencies, int[][] synonyms) {
    int n = names.length;
    List<List<Integer>> adjacent = new ArrayList<>();
    for (int i = 0; i < n; ++i)
      adjacent.add(new ArrayList<>());
    for (int[] edge : synonyms) {
      adjacent.get(edge[0]).add(edge[1]);
      adjacent.get(edge[1]).add(edge[0]);
    }
    boolean[] visited = new boolean[n];
    List<int[]> result = new ArrayList<>();
    for (int start = 0; start < n; ++start) {
      if (visited[start])
        continue;
      visited[start] = true;
      List<Integer> queue = new ArrayList<>();
      queue.add(start);
      int total = 0;
      for (int head = 0; head < queue.size(); ++head) {
        int name = queue.get(head);
        total += frequencies[name];
        for (int other : adjacent.get(name))
          if (!visited[other]) {
            visited[other] = true;
            queue.add(other);
          }
      }
      result.add(new int[] {start, total});
    }
    return result.toArray(new int[0][]);
  }
}
