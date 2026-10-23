import java.util.*;
class BankError extends RuntimeException { public final String Code; public BankError(String code) { super(code); Code=code; } }
class ThreeStacks {
  private final int capacity;
  private final int[] values;
  private final int[] sizes = new int[3];
  private void Check(int stack) {
    if (stack < 0 || stack >= 3)
      throw new BankError("index");
  }
  public ThreeStacks(int supplied) {
    if (supplied < 1 || supplied > 256)
      throw new BankError("capacity");
    capacity = supplied;
    values = new int[3 * supplied];
  }
  public void Push(int stack, int value) {
    Check(stack);
    if (sizes[stack] == capacity)
      throw new BankError("full");
    values[stack * capacity + sizes[stack]] = value;
    ++sizes[stack];
  }
  public int Pop(int stack) {
    Check(stack);
    if (sizes[stack] == 0)
      throw new BankError("empty");
    --sizes[stack];
    return values[stack * capacity + sizes[stack]];
  }
  public int Peek(int stack) {
    Check(stack);
    if (sizes[stack] == 0)
      throw new BankError("empty");
    return values[stack * capacity + sizes[stack] - 1];
  }
  public boolean IsEmpty(int stack) {
    Check(stack);
    return sizes[stack] == 0;
  }
  public boolean IsFull(int stack) {
    Check(stack);
    return sizes[stack] == capacity;
  }
}
