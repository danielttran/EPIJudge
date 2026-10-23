import java.util.*;
abstract class ForkContext {public abstract void Take(int fork);public abstract void Drop(int fork);public abstract void Eat();}
class Solution {
  public void Dine(int role, int philosophers, int bites, ForkContext context) {
    int left = role, right = (role + 1) % philosophers, lower = Math.min(left, right),
        higher = Math.max(left, right);
    for (int bite = 0; bite < bites; ++bite) {
      context.Take(lower);
      context.Take(higher);
      context.Eat();
      context.Drop(higher);
      context.Drop(lower);
    }
  }
}
