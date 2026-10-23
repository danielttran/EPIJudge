import java.util.*;
class Solution {
  public int[] BuildOrder(int projectCount, int[][] dependencies) {
    List<List<Integer>> adjacent = new ArrayList<>();
    for (int i = 0; i < projectCount; ++i)
      adjacent.add(new ArrayList<>());
    int[] indegree = new int[projectCount];
    for (int[] edge : dependencies) {
      adjacent.get(edge[0]).add(edge[1]);
      ++indegree[edge[1]];
    }
    List<Integer> order = new ArrayList<>();
    for (int i = 0; i < projectCount; ++i)
      if (indegree[i] == 0)
        order.add(i);
    for (int head = 0; head < order.size(); ++head)
      for (int dependent : adjacent.get(order.get(head))) {
        --indegree[dependent];
        if (indegree[dependent] == 0)
          order.add(dependent);
      }
    if (order.size() != projectCount)
      return new int[0];
    int[] result = new int[projectCount];
    for (int i = 0; i < projectCount; ++i)
      result[i] = order.get(i);
    return result;
  }
}
