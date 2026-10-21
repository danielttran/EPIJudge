using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public List<(int, int)> OptimumTaskAssignment(List<int> task_durations)
    {
        var values = task_durations.Order().ToList();
        var result = new List<(int, int)>();
        for (int i = 0; i < values.Count / 2; i++)
            result.Add((values[i], values[values.Count - 1 - i]));
        return result;
    }
}
