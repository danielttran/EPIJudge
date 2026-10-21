using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public void Rearrange(List<int> values)
    {
        for (int i = 1; i < values.Count; i++)
        {
            bool wrong = (i % 2 == 1) ? values[i - 1] > values[i] : values[i - 1] < values[i];
            if (wrong)
                (values[i - 1], values[i]) = (values[i], values[i - 1]);
        }
    }
}
