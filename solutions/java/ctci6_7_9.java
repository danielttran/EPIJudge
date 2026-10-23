import java.util.*;
class CircularArray<T> implements Iterable<T> {
  private final ArrayList<T> items;
  private int head;
  public CircularArray(List<T> initialValues) {
    items = new ArrayList<>(initialValues);
  }
  private void checkIndex(int index) {
    if (index < 0 || index >= items.size())
      throw new IndexOutOfBoundsException("index");
  }
  public T Get(int index) {
    checkIndex(index);
    return items.get((head + index) % items.size());
  }
  public void Set(int index, T value) {
    checkIndex(index);
    items.set((head + index) % items.size(), value);
  }
  public void Rotate(int shift) {
    if (items.isEmpty())
      return;
    head = (head + Math.floorMod(shift, items.size())) % items.size();
  }
  public Iterator<T> iterator() {
    return new Iterator<T>() {
      private int cursor;
      public boolean hasNext() {
        return cursor < items.size();
      }
      public T next() {
        if (!hasNext())
          throw new NoSuchElementException();
        return Get(cursor++);
      }
    };
  }
}
