using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public List<(int, int, int)> ComputeSkyline(List<(int, int, int)> buildings)
    {
        var changes = new SortedDictionary<long, List<(int Height, int Delta)>>();
        void Add(long position, int height, int delta)
        {
            if (!changes.TryGetValue(position, out var at))
                changes[position] = at = [];
            at.Add((height, delta));
        }
        foreach (var (left, right, height) in buildings)
        {
            Add(left, height, 1);
            Add((long)right + 1, height, -1);
        }
        var counts = new Dictionary<int, int>();
        var heights = new SortedSet<int>();
        var result = new List<(int, int, int)>();
        long? previous = null;
        int currentHeight = 0;
        foreach (var (position, updates) in changes)
        {
            if (previous is long start && start < position)
            {
                int left = (int)start, right = (int)(position - 1);
                if (result.Count > 0 && result[^1].Item3 == currentHeight && (long)result[^1].Item2 + 1 == left)
                    result[^1] = (result[^1].Item1, right, currentHeight);
                else
                    result.Add((left, right, currentHeight));
            }
            foreach (var (height, delta) in updates)
            {
                counts.TryGetValue(height, out int count);
                count += delta;
                if (count == 0)
                {
                    counts.Remove(height);
                    heights.Remove(height);
                }
                else
                {
                    counts[height] = count;
                    heights.Add(height);
                }
            }
            currentHeight = heights.Count == 0 ? 0 : heights.Max;
            previous = position;
        }
        return result;
    }
}
