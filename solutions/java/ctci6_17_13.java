import java.util.*;
class Solution {
  public List<String> ReSpace(String text, String[] dictionary) {
    Set<String> words = new HashSet<>(Arrays.asList(dictionary));
    int maximum = 0;
    for (String word : words)
      maximum = Math.max(maximum, word.length());
    int[] cost = new int[text.length() + 1], previous = new int[text.length() + 1];
    for (int end = 1; end <= text.length(); ++end) {
      cost[end] = cost[end - 1] + 1;
      previous[end] = end - 1;
      for (int length = 1; length <= maximum && length <= end; ++length) {
        int start = end - length;
        if (words.contains(text.substring(start, end)) && cost[start] < cost[end]) {
          cost[end] = cost[start];
          previous[end] = start;
        }
      }
    }
    List<String> result = new ArrayList<>();
    for (int end = text.length(); end > 0; end = previous[end])
      result.add(text.substring(previous[end], end));
    Collections.reverse(result);
    return result;
  }
}
