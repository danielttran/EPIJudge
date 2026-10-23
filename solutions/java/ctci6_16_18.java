import java.util.*;
class Solution {
  public boolean MatchesPattern(String pattern, String text) {
    if (pattern.length() == 0)
      return text.length() == 0;
    int countA = 0;
    for (char symbol : pattern.toCharArray())
      if (symbol == 'a')
        ++countA;
    int countB = pattern.length() - countA, maximum = countA == 0 ? 0 : text.length() / countA;
    for (int lengthA = 0; lengthA <= maximum; ++lengthA) {
      int remaining = text.length() - countA * lengthA;
      if (countB == 0 ? remaining != 0 : remaining % countB != 0)
        continue;
      int lengthB = countB == 0 ? 0 : remaining / countB;
      String a = null, b = null;
      int offset = 0;
      boolean valid = true;
      for (char symbol : pattern.toCharArray()) {
        int length = symbol == 'a' ? lengthA : lengthB;
        String part = text.substring(offset, offset + length);
        if (symbol == 'a') {
          if (a == null)
            a = part;
          else if (!a.equals(part)) {
            valid = false;
            break;
          }
        } else {
          if (b == null)
            b = part;
          else if (!b.equals(part)) {
            valid = false;
            break;
          }
        }
        offset += length;
      }
      if (valid && offset == text.length())
        return true;
    }
    return false;
  }
}
