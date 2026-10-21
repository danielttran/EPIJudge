using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public int FindNearestRepetition(List<string> paragraph)
    {
        var last = new Dictionary<string, int>();
        int best = int.MaxValue;
        for (int i = 0; i < paragraph.Count; i++)
        {
            if (last.TryGetValue(paragraph[i], out int previous))
                best = Math.Min(best, i - previous);
            last[paragraph[i]] = i;
        }
        return best == int.MaxValue ? -1 : best;
    }
}
