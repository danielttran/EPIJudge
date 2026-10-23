import java.util.*;
class Solution {
  public double Calculate(String expression) {
    double total = 0, term = 0;
    char op = '+';
    int index = 0;
    while (index < expression.length()) {
      int number = 0;
      while (index < expression.length() && expression.charAt(index) >= '0'
          && expression.charAt(index) <= '9') {
        number = number * 10 + expression.charAt(index) - '0';
        index++;
      }
      if (op == '+') {
        total += term;
        term = number;
      } else if (op == '-') {
        total += term;
        term = -number;
      } else if (op == '*')
        term *= number;
      else
        term /= number;
      if (index < expression.length())
        op = expression.charAt(index++);
    }
    return total + term;
  }
}
