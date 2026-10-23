import java.util.*;
class Solution {
  public int CountDigitTwos(int n) {
    long total = 0;
    for (long place = 1; place <= n; place *= 10) {
      long high = n / (place * 10), digit = (n / place) % 10, low = n % place;
      total += high * place;
      if (digit == 2)
        total += low + 1;
      else if (digit > 2)
        total += place;
    }
    return (int) total;
  }
}
