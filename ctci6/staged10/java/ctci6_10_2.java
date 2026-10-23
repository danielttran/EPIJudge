import java.util.*;
class Solution {
  public List<String> GroupAnagrams(String[] words) {
    int n = words.length;
    String[] original = words.clone(), keys = new String[n];
    Integer[] order = new Integer[n];
    for (int i = 0; i < n; ++i) {
      char[] letters = words[i].toCharArray();
      Arrays.sort(letters);
      keys[i] = new String(letters);
      order[i] = i;
    }
    Arrays.sort(order, (a, b) -> keys[a].compareTo(keys[b]));
    for (int i = 0; i < n; ++i)
      words[i] = original[order[i]];
    return new ArrayList<>(Arrays.asList(words));
  }
}
