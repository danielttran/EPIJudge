using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public int FindMaxSimultaneousEvents(List<(int, int)> events)
    {
        var endpoints = new List<(int Time, int Delta)>();
        foreach (var (start, finish) in events)
        {
            endpoints.Add((start, 1));
            endpoints.Add((finish, -1));
        }
        endpoints.Sort((a, b) => a.Time != b.Time ? a.Time.CompareTo(b.Time) : b.Delta.CompareTo(a.Delta));
        int current = 0, maximum = 0;
        foreach (var endpoint in endpoints)
        {
            current += endpoint.Delta;
            maximum = Math.Max(maximum, current);
        }
        return maximum;
    }
}
