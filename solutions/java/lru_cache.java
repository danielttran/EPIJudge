package epi;

import epi.test_framework.EpiTest;
import epi.test_framework.EpiUserType;
import epi.test_framework.GenericTest;
import epi.test_framework.TestFailure;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public class LruCache {
  private final int capacity;
  private final LinkedHashMap<Integer, Integer> entries =
      new LinkedHashMap<>(16, 0.75f, true);

  LruCache(final int capacity) { this.capacity = Math.max(0, capacity); }

  public Integer lookup(Integer key) {
    Integer price = entries.get(key);
    return price == null ? -1 : price;
  }

  public void insert(Integer key, Integer value) {
    if (entries.containsKey(key)) {
      entries.get(key);
      return;
    }
    if (capacity == 0) return;
    entries.put(key, value);
    if (entries.size() > capacity) {
      Iterator<Map.Entry<Integer, Integer>> oldest = entries.entrySet().iterator();
      oldest.next();
      oldest.remove();
    }
  }

  public Boolean erase(Object key) { return entries.remove(key) != null; }

  @EpiUserType(ctorParams = {String.class, int.class, int.class})
  public static class Op {
    String code;
    int arg1;
    int arg2;
    public Op(String code, int arg1, int arg2) {
      this.code = code;
      this.arg1 = arg1;
      this.arg2 = arg2;
    }
    @Override
    public String toString() { return code + "(" + arg1 + ", " + arg2 + ")"; }
  }

  @EpiTest(testDataFile = "lru_cache.tsv")
  public static void lruCacheTester(List<Op> commands) throws TestFailure {
    LruCache cache = new LruCache(0);
    for (int index = 0; index < commands.size(); index++) {
      Op operation = commands.get(index);
      switch (operation.code) {
        case "LruCache":
          cache = new LruCache(operation.arg1);
          break;
        case "insert":
          cache.insert(operation.arg1, operation.arg2);
          break;
        case "lookup": {
          int actual = cache.lookup(operation.arg1);
          if (actual != operation.arg2) {
            throw new TestFailure("The cached price differs from its expected result.")
                .withProperty(TestFailure.PropertyName.COMMAND, operation)
                .withMismatchInfo(index, operation.arg2, actual);
          }
          break;
        }
        case "erase": {
          int actual = cache.erase(operation.arg1) ? 1 : 0;
          if (actual != operation.arg2) {
            throw new TestFailure("Erasure existence differs from its expected result.")
                .withProperty(TestFailure.PropertyName.COMMAND, operation)
                .withMismatchInfo(index, operation.arg2, actual);
          }
          break;
        }
        default:
          throw new TestFailure("Unknown cache operation: " + operation.code)
              .withProperty(TestFailure.PropertyName.COMMAND, operation);
      }
    }
  }

  public static void main(String[] args) {
    System.exit(GenericTest.runFromAnnotations(args, "LruCache.java", LruCache.class).ordinal());
  }
}
