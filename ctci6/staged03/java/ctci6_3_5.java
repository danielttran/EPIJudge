import java.util.*;
class BankError extends RuntimeException { public final String Code; public BankError(String code) { super(code); Code=code; } }
class IntStack {
private final ArrayDeque<Integer> values = new ArrayDeque<>();
public void Push(int value) { values.push(value); }
public int Pop() { if (values.isEmpty()) throw new BankError("empty"); return values.pop(); }
public int Peek() { if (values.isEmpty()) throw new BankError("empty"); return values.peek(); }
public boolean IsEmpty() { return values.isEmpty(); }
}
class Solution {
  public void SortStack(IntStack stack) {
    var spare = new IntStack();
    while (!stack.IsEmpty()) {
      int value = stack.Pop();
      while (!spare.IsEmpty() && spare.Peek() > value)
        stack.Push(spare.Pop());
      spare.Push(value);
    }
    while (!spare.IsEmpty())
      stack.Push(spare.Pop());
  }
}
