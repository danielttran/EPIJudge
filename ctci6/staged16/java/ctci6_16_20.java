import java.util.*;
class Solution {
  public List<String> T9Words(String digits, String[] dictionary) {
    String mapping = "22233344455566677778889999";
    List<String> result = new ArrayList<>();
    for (String word : dictionary) {
      if (word.length() != digits.length())
        continue;
      boolean valid = true;
      for (int i = 0; i < word.length(); ++i)
        if (mapping.charAt(word.charAt(i) - 'a') != digits.charAt(i)) {
          valid = false;
          break;
        }
      if (valid)
        result.add(word);
    }
    return result;
  }
}
