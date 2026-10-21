using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public void RandomSampling(int k, List<int> values)
    {
        for (int i = 0; i < k; i++)
        {
            int j = Random.Shared.Next(i, values.Count);
            (values[i], values[j]) = (values[j], values[i]);
        }
    }
}
