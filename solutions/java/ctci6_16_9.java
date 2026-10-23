import java.util.*;
class Solution {
  public int AdditionOnlyArithmetic(int first, int second, String operation) {
    class Negator {
      int opposite(int value) {
        int step = value < 0 ? 1 : -1, result = 0;
        while (value != 0) {
          value += step;
          result += step;
        }
        return result;
      }
    }
    Negator negator = new Negator();
    if (operation.equals("subtract"))
      return first + negator.opposite(second);
    if (operation.equals("multiply")) {
      int count = second < 0 ? negator.opposite(second) : second,
          addend = second < 0 ? negator.opposite(first) : first, result = 0;
      while (count > 0) {
        result += addend;
        count += -1;
      }
      return result;
    }
    int remaining = first < 0 ? negator.opposite(first) : first,
        divisor = second < 0 ? negator.opposite(second) : second,
        remove = negator.opposite(divisor), step = (first < 0) == (second < 0) ? 1 : -1,
        quotient = 0;
    while (remaining + remove >= 0) {
      remaining += remove;
      quotient += step;
    }
    return quotient;
  }
}
