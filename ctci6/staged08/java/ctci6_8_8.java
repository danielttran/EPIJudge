import java.util.*;
class Solution {
  public List<String> PermutationsWithDuplicates(String text) {
    int[] counts = new int[26];
    for (char c : text.toCharArray())
      ++counts[c - 'a'];
    char[] buffer = new char[text.length()];
    List<String> result = new ArrayList<>();
    class Search {
      void Visit(int depth) {
        if (depth == buffer.length) {
          result.add(new String(buffer));
          return;
        }
        for (int letter = 0; letter < 26; ++letter) {
          if (counts[letter] > 0) {
            --counts[letter];
            buffer[depth] = (char) ('a' + letter);
            Visit(depth + 1);
            ++counts[letter];
          }
        }
      }
    }
    new Search().Visit(0);
    return result;
  }
}
