import java.util.*;
class Solution {
  public int[][] SparseSimilarities(int[] documentIds, int[][] documents) {
    int n = documentIds.length;
    Map<Integer, List<Integer>> postings = new HashMap<>();
    for (int i = 0; i < n; ++i)
      for (int word : documents[i])
        postings.computeIfAbsent(word, k -> new ArrayList<>()).add(i);
    Map<Integer, Integer> intersections = new HashMap<>();
    for (List<Integer> posting : postings.values())
      for (int a = 0; a < posting.size(); ++a)
        for (int b = a + 1; b < posting.size(); ++b) {
          int key = posting.get(a) * n + posting.get(b);
          intersections.put(key, intersections.getOrDefault(key, 0) + 1);
        }
    List<int[]> result = new ArrayList<>();
    for (var entry : intersections.entrySet()) {
      int left = entry.getKey() / n, right = entry.getKey() % n, count = entry.getValue(),
          a = documentIds[left], b = documentIds[right];
      result.add(new int[] {Math.min(a, b), Math.max(a, b), count,
          documents[left].length + documents[right].length - count});
    }
    result.sort((a, b) -> {
      int first = Integer.compare(a[0], b[0]);
      return first != 0 ? first : Integer.compare(a[1], b[1]);
    });
    return result.toArray(new int[0][]);
  }
}
