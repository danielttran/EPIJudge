import java.util.*;
abstract class ResourceLock {public abstract void Lock();public abstract void Unlock();}
abstract class LockPool {public abstract ResourceLock Get(int resource);}
class DeadlockFreeLocks {
  private final int count;
  private final LockPool pool;
  private final int[][] orders = new int[4][0];
  private final int[] next = new int[4];
  public DeadlockFreeLocks(int resourceCount, LockPool pool) {
    count = resourceCount;
    this.pool = pool;
  }
  public boolean Declare(int owner, int[] order) {
    if (owner < 0 || owner >= 4)
      return false;
    boolean[] seen = new boolean[count];
    for (int resource : order) {
      if (resource < 0 || resource >= count || seen[resource])
        return false;
      seen[resource] = true;
    }
    boolean[][] reach = new boolean[count][count];
    for (int candidate = 0; candidate < 4; ++candidate) {
      int[] path = candidate == owner ? order : orders[candidate];
      for (int i = 1; i < path.length; ++i)
        reach[path[i - 1]][path[i]] = true;
    }
    for (int middle = 0; middle < count; ++middle)
      for (int first = 0; first < count; ++first)
        for (int second = 0; second < count; ++second)
          reach[first][second] |= reach[first][middle] && reach[middle][second];
    for (int i = 0; i < count; ++i)
      if (reach[i][i])
        return false;
    orders[owner] = order.clone();
    next[owner] = 0;
    return true;
  }
  public ResourceLock GetLock(int owner, int resource) {
    if (owner < 0 || owner >= 4)
      return null;
    int[] path = orders[owner];
    if (next[owner] == path.length || path[next[owner]] != resource)
      return null;
    next[owner]++;
    return pool.Get(resource);
  }
}
