using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public int LongestContainedRange(List<int> A)
    {
        var unseen = A.ToHashSet();
        int best = 0;
        foreach (int value in A)
        {
            if (!unseen.Remove(value))
                continue;
            int size = 1;
            for (long x = (long)value - 1; x >= int.MinValue && unseen.Remove((int)x); x--)
                size++;
            for (long x = (long)value + 1; x <= int.MaxValue && unseen.Remove((int)x); x++)
                size++;
            best = Math.Max(best, size);
        }
        return best;
    }
}
