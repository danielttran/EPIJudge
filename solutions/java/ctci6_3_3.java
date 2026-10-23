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
class SetOfStacks {
  private final int capacity;
  private final ArrayList<ArrayList<Integer>> stacks = new ArrayList<>();
  public SetOfStacks(int supplied) {
    if (supplied < 1 || supplied > 256)
      throw new BankError("capacity");
    capacity = supplied;
  }
  public void Push(int value) {
    int last = stacks.size() - 1;
    if (last < 0 || stacks.get(last).size() == capacity) {
      stacks.add(new ArrayList<>());
      ++last;
    }
    stacks.get(last).add(value);
  }
  public int Pop() {
    if (stacks.size() == 0)
      throw new BankError("empty");
    int last = stacks.size() - 1;
    int value = stacks.get(last).get(stacks.get(last).size() - 1);
    stacks.get(last).remove(stacks.get(last).size() - 1);
    if (stacks.get(last).size() == 0) {
      stacks.remove(last);
    }
    return value;
  }
  public int PopAt(int index) {
    if (index < 0 || index >= stacks.size())
      throw new BankError("index");
    int value = stacks.get(index).get(stacks.get(index).size() - 1);
    stacks.get(index).remove(stacks.get(index).size() - 1);
    for (int i = index; i + 1 < stacks.size(); ++i) {
      int bottom = stacks.get(i + 1).get(0);
      stacks.get(i + 1).remove(0);
      stacks.get(i).add(bottom);
    }
    int last = stacks.size() - 1;
    if (stacks.get(last).size() == 0) {
      stacks.remove(last);
    }
    return value;
  }
  public boolean IsEmpty() {
    return stacks.size() == 0;
  }
}
