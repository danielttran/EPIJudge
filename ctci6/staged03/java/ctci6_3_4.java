import java.util.*;
class BankError extends RuntimeException { public final String Code; public BankError(String code) { super(code); Code=code; } }
class TwoStackQueue {
  private final ArrayDeque<Integer> newest = new ArrayDeque<>(), oldest = new ArrayDeque<>();
  private void Shift() {
    if (oldest.size() == 0) {
      while (!(newest.size() == 0)) {
        oldest.push(newest.pop());
      }
    }
  }
  public TwoStackQueue() {
  }
  public void Add(int value) {
    newest.push(value);
  }
  public int Remove() {
    Shift();
    if (oldest.size() == 0)
      throw new BankError("empty");
    return oldest.pop();
  }
  public int Peek() {
    Shift();
    if (oldest.size() == 0)
      throw new BankError("empty");
    return oldest.peek();
  }
  public int Size() {
    return newest.size() + oldest.size();
  }
}
