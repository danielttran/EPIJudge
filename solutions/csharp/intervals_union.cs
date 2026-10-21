public class Solution
{
    public List<(int, bool, int, bool)> UnionOfIntervals(List<(int, bool, int, bool)> intervals)
    {
        var ordered = intervals.OrderBy(x => x.Item1).ThenByDescending(x => x.Item2).ToArray();
        var result = new List<(int, bool, int, bool)>();
        foreach (var next in ordered)
        {
            if (result.Count == 0)
            {
                result.Add(next);
                continue;
            }
            var current = result[^1];
            bool overlaps = next.Item1 < current.Item3 ||
                (next.Item1 == current.Item3 && (current.Item4 || next.Item2));
            if (!overlaps)
            {
                result.Add(next);
                continue;
            }
            bool leftClosed = current.Item2 || (next.Item1 == current.Item1 && next.Item2);
            if (next.Item3 > current.Item3)
                current = (current.Item1, leftClosed, next.Item3, next.Item4);
            else if (next.Item3 == current.Item3)
                current = (current.Item1, leftClosed, current.Item3, current.Item4 || next.Item4);
            else
                current = (current.Item1, leftClosed, current.Item3, current.Item4);
            result[^1] = current;
        }
        return result;
    }
}
