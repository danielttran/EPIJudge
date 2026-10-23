import java.util.*;
class Solution {
  public List<String> GenerateParentheses(int pairs) {
    char[] buffer = new char[2 * pairs];
    List<String> result = new ArrayList<>();
    class Search {
      void Visit(int opened, int closed) {
        int position = opened + closed;
        if (position == buffer.length) {
          result.add(new String(buffer));
          return;
        }
        if (opened < pairs) {
          buffer[position] = '(';
          Visit(opened + 1, closed);
        }
        if (closed < opened) {
          buffer[position] = ')';
          Visit(opened, closed + 1);
        }
      }
    }
    new Search().Visit(0, 0);
    return result;
  }
}
