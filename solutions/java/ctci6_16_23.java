import java.util.*;
abstract class Rand5Source { public abstract int Next(); }
class Solution {
  public int UniformSeven(Rand5Source source) {
    while (true) {
      int state = 5 * source.Next() + source.Next();
      if (state < 21)
        return state % 7;
    }
  }
}
