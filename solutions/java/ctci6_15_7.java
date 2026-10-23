import java.util.*;
abstract class FizzContext {public abstract void Wait(int gate);public abstract void Signal(int gate);public abstract void Print(int value);}
class Solution {
  public void RunFizzBuzz(int role, int limit, FizzContext context) {
    java.util.function.IntUnaryOperator owner = value
        -> value % 15 == 0 ? 3
        : value % 3 == 0   ? 1
        : value % 5 == 0   ? 2
                           : 0;
    for (int value = 1; value <= limit; ++value) {
      if (owner.applyAsInt(value) != role)
        continue;
      context.Wait(role);
      context.Print(value);
      if (value < limit)
        context.Signal(owner.applyAsInt(value + 1));
    }
  }
}
