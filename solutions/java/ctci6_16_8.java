import java.util.*;
class Solution {
  public String EnglishInteger(int value) {
    if (value == 0)
      return "Zero";
    String[] small = {"Zero", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight",
                 "Nine", "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen",
                 "Seventeen", "Eighteen", "Nineteen"},
             tens = {"", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty",
                 "Ninety"},
             scales = {"", "Thousand", "Million", "Billion"};
    long magnitude = value;
    if (magnitude < 0)
      magnitude = -magnitude;
    List<String> groups = new ArrayList<>();
    int scale = 0;
    while (magnitude > 0) {
      int chunk = (int) (magnitude % 1000);
      if (chunk != 0) {
        List<String> words = new ArrayList<>();
        if (chunk >= 100) {
          words.add(small[chunk / 100]);
          words.add("Hundred");
          chunk %= 100;
        }
        if (chunk >= 20) {
          words.add(tens[chunk / 10]);
          chunk %= 10;
        }
        if (chunk != 0)
          words.add(small[chunk]);
        if (scale != 0)
          words.add(scales[scale]);
        groups.add(String.join(" ", words));
      }
      magnitude /= 1000;
      ++scale;
    }
    Collections.reverse(groups);
    return (value < 0 ? "Negative " : "") + String.join(" ", groups);
  }
}
