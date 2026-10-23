import java.util.*;
class Solution {
  public List<String> PermutationsDistinct(String text) {
    char[] chars = text.toCharArray();
    List<String> result = new ArrayList<>();
    class Search {
      void Visit(int depth) {
        if (depth == chars.length) {
          result.add(new String(chars));
          return;
        }
        for (int i = depth; i < chars.length; ++i) {
          char temporary = chars[depth];
          chars[depth] = chars[i];
          chars[i] = temporary;
          Visit(depth + 1);
          temporary = chars[depth];
          chars[depth] = chars[i];
          chars[i] = temporary;
        }
      }
    }
    new Search().Visit(0);
    return result;
  }
}
