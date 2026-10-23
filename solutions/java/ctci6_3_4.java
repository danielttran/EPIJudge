import java.util.*;
class BankError extends RuntimeException { public final String Code; public BankError(String code) { super(code); Code=code; } }
class IntStack {
private final ArrayDeque<Integer> values = new ArrayDeque<>();
public void Push(int value) { values.push(value); }
public int Pop() { if (values.isEmpty()) throw new BankError("empty"); return values.pop(); }
public int Peek() { if (values.isEmpty()) throw new BankError("empty"); return values.peek(); }
public boolean IsEmpty() { return values.isEmpty(); }
}
final class Animal { public final int Id; public final String Species; public Animal(int id,String species) { Id=id; Species=species; } }
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
