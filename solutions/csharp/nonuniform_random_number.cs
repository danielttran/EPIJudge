using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public int NonuniformRandomNumberGeneration(List<int> values, List<double> probabilities)
    {
        double target = Random.Shared.NextDouble(), cumulative = 0;
        for (int i = 0; i < values.Count - 1; i++)
        {
            cumulative += probabilities[i];
            if (target < cumulative)
                return values[i];
        }
        return values[^1];
    }
}
