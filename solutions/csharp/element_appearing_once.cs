using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public int FindElementAppearsOnce(List<int> A)
    {
        int once = 0, twice = 0;
        foreach (int value in A)
        {
            once = (once ^ value) & ~twice;
            twice = (twice ^ value) & ~once;
        }
        return once;
    }
}
