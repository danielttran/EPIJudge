import java.util.*;
class LRUCache {
  private final int capacity;
  private final LinkedHashMap<Integer, String> entries = new LinkedHashMap<>(16, 0.75f, true);
  public LRUCache(int capacity) {
    this.capacity = capacity;
  }
  public String Get(int key) {
    return entries.get(key);
  }
  public void Set(int key, String value) {
    entries.put(key, value);
    if (entries.size() > capacity)
      entries.remove(entries.keySet().iterator().next());
  }
}
