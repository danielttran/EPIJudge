using System;
using System.Collections.Generic;
using System.Text;
public abstract class ResourceLock {public abstract void Lock();public abstract void Unlock();}
public abstract class LockPool {public abstract ResourceLock Get(int resource);}
public class DeadlockFreeLocks
{
    private readonly int count;
    private readonly LockPool pool;
    private readonly int[][] orders = Enumerable.Range(0, 4)
                                          .Select(
                                              _ => Array.Empty<int>())
                                          .ToArray();
    private readonly int[] next = new int[4];
    public DeadlockFreeLocks(int resourceCount, LockPool pool)
    {
        count = resourceCount;
        this.pool = pool;
    }
    public bool Declare(int owner, int[] order)
    {
        if (owner < 0 || owner >= 4)
            return false;
        var seen = new bool[count];
        foreach (int resource in order)
        {
            if (resource < 0 || resource >= count || seen[resource])
                return false;
            seen[resource] = true;
        }
        var reach = new bool[count, count];
        for (int candidate = 0; candidate < 4; ++candidate)
        {
            var path = candidate == owner ? order : orders[candidate];
            for (int i = 1; i < path.Length; ++i)
                reach[path[i - 1], path[i]] = true;
        }
        for (int middle = 0; middle < count; ++middle)
            for (int first = 0; first < count; ++first)
                for (int second = 0; second < count; ++second)
                    reach[first, second] |= reach[first, middle] && reach[middle, second];
        for (int i = 0; i < count; ++i)
            if (reach[i, i])
                return false;
        orders[owner] = order.ToArray();
        next[owner] = 0;
        return true;
    }
    public ResourceLock? GetLock(int owner, int resource)
    {
        if (owner < 0 || owner >= 4)
            return null;
        var path = orders[owner];
        if (next[owner] == path.Length || path[next[owner]] != resource)
            return null;
        next[owner]++;
        return pool.Get(resource);
    }
}
