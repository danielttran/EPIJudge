using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public List<int> RandomSubset(int n, int k)
    {
        var moved = new Dictionary<int, int>();
        var result = new List<int>(k);
        for (int i = 0; i < k; i++)
        {
            int selected = Random.Shared.Next(i, n);
            int chosen = moved.GetValueOrDefault(selected, selected);
            moved[selected] = moved.GetValueOrDefault(i, i);
            result.Add(chosen);
        }
        return result;
    }
}
