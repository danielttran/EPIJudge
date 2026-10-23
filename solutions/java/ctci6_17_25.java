import java.util.*;
class Solution {
  public List<String> LargestWordRectangle(String[] words) {
    Set<String> seen = new HashSet<>();
    List<List<String>> groups = new ArrayList<>();
    for (int i = 0; i <= 5; ++i)
      groups.add(new ArrayList<>());
    int maximum = 0;
    for (String word : words)
      if (seen.add(word)) {
        groups.get(word.length()).add(word);
        maximum = Math.max(maximum, word.length());
      }
    for (int area = maximum * maximum; area > 0; --area)
      for (int height = 1; height <= maximum; ++height) {
        if (area % height != 0)
          continue;
        int width = area / height;
        if (width > maximum || groups.get(width).isEmpty() || groups.get(height).isEmpty())
          continue;
        Set<String> prefixes = new HashSet<>();
        for (String word : groups.get(height))
          for (int length = 1; length <= height; ++length)
            prefixes.add(word.substring(0, length));
        List<String> rows = new ArrayList<>();
        int targetHeight = height, targetWidth = width;
        class Search {
          boolean run() {
            if (rows.size() == targetHeight)
              return true;
            for (String word : groups.get(targetWidth)) {
              rows.add(word);
              boolean valid = true;
              for (int column = 0; column < targetWidth; ++column) {
                StringBuilder prefix = new StringBuilder();
                for (String row : rows)
                  prefix.append(row.charAt(column));
                if (!prefixes.contains(prefix.toString())) {
                  valid = false;
                  break;
                }
              }
              if (valid && run())
                return true;
              rows.remove(rows.size() - 1);
            }
            return false;
          }
        }
        if (new Search().run())
          return rows;
      }
    return new ArrayList<>();
  }
}
