import java.util.*;
class Solution {
  public int WordDistance(String[] words, String first, String second) {
    int lastFirst = -1, lastSecond = -1, best = words.length + 1;
    for (int i = 0; i < words.length; ++i) {
      if (words[i].equals(first)) {
        lastFirst = i;
        if (lastSecond >= 0)
          best = Math.min(best, i - lastSecond);
      } else if (words[i].equals(second)) {
        lastSecond = i;
        if (lastFirst >= 0)
          best = Math.min(best, i - lastFirst);
      }
    }
    return best == words.length + 1 ? -1 : best;
  }
}
