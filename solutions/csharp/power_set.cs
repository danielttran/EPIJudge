using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public List<List<int>> GeneratePowerSet(List<int> input_set)
    {
        var result = new List<List<int>> { new() };
        foreach (int value in input_set)
        {
            int previousCount = result.Count;
            for (int i = 0; i < previousCount; i++)
            {
                var subset = new List<int>(result[i]) { value };
                result.Add(subset);
            }
        }
        return result;
    }
}
