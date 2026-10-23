import java.util.*;
class Solution {
  public int[][] MultiSearch(String text, String[] patterns) {
    List<int[]> result = new ArrayList<>();
    for (String pattern : patterns) {
      List<Integer> positions = new ArrayList<>();
      for (int start = 0; start + pattern.length() <= text.length(); ++start)
        if (text.startsWith(pattern, start))
          positions.add(start);
      int[] row = new int[positions.size()];
      for (int i = 0; i < row.length; ++i)
        row[i] = positions.get(i);
      result.add(row);
    }
    return result.toArray(new int[0][]);
  }
}
