import java.util.*;
class Solution {
  public boolean HasDirectedRoute(int nodeCount, int[][] edges, int start, int target) {
    if (start == target)
      return true;
    List<List<Integer>> adjacent = new ArrayList<>();
    for (int i = 0; i < nodeCount; ++i)
      adjacent.add(new ArrayList<>());
    for (int[] edge : edges)
      adjacent.get(edge[0]).add(edge[1]);
    boolean[] visited = new boolean[nodeCount];
    List<Integer> queue = new ArrayList<>();
    queue.add(start);
    visited[start] = true;
    for (int head = 0; head < queue.size(); ++head)
      for (int neighbor : adjacent.get(queue.get(head)))
        if (!visited[neighbor]) {
          if (neighbor == target)
            return true;
          visited[neighbor] = true;
          queue.add(neighbor);
        }
    return false;
  }
}
