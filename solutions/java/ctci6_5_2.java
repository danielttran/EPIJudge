import java.util.*;
class Solution {
  public String BinaryFraction(double number) {
    if (number <= 0 || number >= 1)
      return "ERROR";
    var result = new StringBuilder(".");
    for (int i = 0; i < 31; ++i) {
      number *= 2;
      boolean bit = number >= 1;
      result.append(bit ? '1' : '0');
      if (bit)
        --number;
      if (number == 0)
        return result.toString();
    }
    return "ERROR";
  }
}
