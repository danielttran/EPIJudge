import java.util.*;
class Solution {
  public int[] WordFrequencies(String[] book, String[] queries) {
    Map<String, Integer> counts = new HashMap<>();
    for (String word : book) {
      String key = word.toLowerCase(Locale.ROOT);
      counts.put(key, counts.getOrDefault(key, 0) + 1);
    }
    int[] result = new int[queries.length];
    for (int i = 0; i < queries.length; ++i)
      result[i] = counts.getOrDefault(queries[i].toLowerCase(Locale.ROOT), 0);
    return result;
  }
}
