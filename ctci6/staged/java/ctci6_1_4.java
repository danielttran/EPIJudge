import java.util.*;
class Solution {
  public boolean PalindromePermutation(String text) {
    int[] counts = new int[128];
    for (int i = 0; i < text.length(); ++i) {
      int code = text.charAt(i);
      if (code >= 65 && code <= 90)
        code += 32;
      if (code >= 97 && code <= 122)
        ++counts[code];
    }
    int odd = 0;
    for (int code = 97; code <= 122; ++code)
      odd += counts[code] % 2;
    return odd <= 1;
  }
}
