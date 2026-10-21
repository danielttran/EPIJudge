using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public List<int> ComputeRandomPermutation(int n)
    {
        var values = Enumerable.Range(0, n).ToList();
        for (int i = 0; i < n; i++)
        {
            int selected = Random.Shared.Next(i, n);
            (values[i], values[selected]) = (values[selected], values[i]);
        }
        return values;
    }
}
