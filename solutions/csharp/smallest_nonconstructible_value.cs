using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public int SmallestNonconstructibleValue(List<int> A)
    {
        var values = A.Order().ToList();
        long covered = 0;
        foreach (int value in values)
        {
            if (value > covered + 1)
                break;
            covered += value;
        }
        return checked((int)(covered + 1));
    }
}
