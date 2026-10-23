import java.util.*;
class Solution {
  public String LongestComposedWord(String[] words) {
    Set<String> dictionary = new HashSet<>(Arrays.asList(words));
    String best = "";
    for (String word : words) {
      int[] dp = new int[word.length() + 1];
      Arrays.fill(dp, -1);
      dp[0] = 0;
      for (int end = 1; end <= word.length(); ++end)
        for (int start = 0; start < end; ++start)
          if (dp[start] >= 0 && dictionary.contains(word.substring(start, end)))
            dp[end] = Math.max(dp[end], dp[start] + 1);
      if (dp[word.length()] >= 2
          && (word.length() > best.length()
              || (word.length() == best.length() && word.compareTo(best) < 0)))
        best = word;
    }
    return best;
  }
}
