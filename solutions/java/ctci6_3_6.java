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
class AnimalShelter {
  private static class Entry {
    public Animal Value;
    public int Order;
    public Entry Next;
    public Entry(Animal value, int order) {
      Value = value;
      Order = order;
    }
  }
  private final Entry[] heads = new Entry[2], tails = new Entry[2];
  private int order = 0, count = 0;
  private int Oldest() {
    if (heads[0] == null)
      return 1;
    if (heads[1] == null)
      return 0;
    return heads[0].Order < heads[1].Order ? 0 : 1;
  }
  private Animal Take(int slot) {
    var entry = heads[slot];
    if (entry == null)
      return null;
    heads[slot] = entry.Next;
    if (heads[slot] == null)
      tails[slot] = null;
    --count;
    return entry.Value;
  }

  public AnimalShelter() {
  }
  public void Enqueue(Animal animal) {
    int slot;
    if (animal.Species.equals("dog"))
      slot = 0;
    else if (animal.Species.equals("cat"))
      slot = 1;
    else
      throw new BankError("species");
    var entry = new Entry(animal, order++);
    if (tails[slot] == null)
      heads[slot] = entry;
    else
      tails[slot].Next = entry;
    tails[slot] = entry;
    ++count;
  }
  public Animal DequeueAny() {
    return Take(Oldest());
  }
  public Animal DequeueDog() {
    return Take(0);
  }
  public Animal DequeueCat() {
    return Take(1);
  }
  public Animal Peek() {
    return heads[Oldest()] == null ? null : heads[Oldest()].Value;
  }
  public int Size() {
    return count;
  }
}
