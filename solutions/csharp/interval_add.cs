public class Solution
{
    public List<(int, int)> AddInterval(List<(int, int)> disjoint_intervals, (int, int) new_interval)
    {
        var result = new List<(int, int)>();
        int index = 0;
        while (index < disjoint_intervals.Count && disjoint_intervals[index].Item2 < new_interval.Item1)
            result.Add(disjoint_intervals[index++]);
        while (index < disjoint_intervals.Count && disjoint_intervals[index].Item1 <= new_interval.Item2)
        {
            var next = disjoint_intervals[index++];
            new_interval = (Math.Min(new_interval.Item1, next.Item1), Math.Max(new_interval.Item2, next.Item2));
        }
        result.Add(new_interval);
        while (index < disjoint_intervals.Count)
            result.Add(disjoint_intervals[index++]);
        return result;
    }
}
