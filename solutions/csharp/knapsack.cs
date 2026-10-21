public class Solution
{
    public int OptimumSubjectToCapacity(List<(int, int)> items, int capacity)
    {
        var best = new int[capacity + 1];
        foreach (var (weight, value) in items)
            for (int available = capacity; available >= weight; available--)
                best[available] = Math.Max(best[available], best[available - weight] + value);
        return best[capacity];
    }
}
