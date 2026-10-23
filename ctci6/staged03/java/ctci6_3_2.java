import java.util.*;
class BankError extends RuntimeException { public final String Code; public BankError(String code) { super(code); Code=code; } }
class MinStack {
  private static class Entry {
    public int Value, Minimum;
    public Entry Next;
    public Entry(int value, int minimum, Entry next) {
      Value = value;
      Minimum = minimum;
      Next = next;
    }
  }
  private Entry top;

  public MinStack() {
  }
  public void Push(int value) {
    int minimum = top == null ? value : Math.min(value, top.Minimum);
    top = new Entry(value, minimum, top);
  }
  public int Pop() {
    if (top == null)
      throw new BankError("empty");
    int value = top.Value;
    top = top.Next;
    return value;
  }
  public int Peek() {
    if (top == null)
      throw new BankError("empty");
    return top.Value;
  }
  public int GetMin() {
    if (top == null)
      throw new BankError("empty");
    return top.Minimum;
  }
  public boolean IsEmpty() {
    return top == null;
  }
}
