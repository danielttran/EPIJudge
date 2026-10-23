import java.util.*;
class Solution {
  public String Compress(String text) {
    StringBuilder output = new StringBuilder();
    int n = text.length();
    for (int start = 0; start < n;) {
      int end = start + 1;
      while (end < n && text.charAt(end) == text.charAt(start))
        ++end;
      output.append(text.charAt(start));
      output.append(end - start);
      start = end;
    }
    return output.length() < n ? output.toString() : text;
  }
}
