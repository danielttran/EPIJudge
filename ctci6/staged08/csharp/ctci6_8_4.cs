using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public List<List<int>> PowerSet(int[] values)
    {
        var result = new List<List<int>> { new() };
        foreach (int value in values)
        {
            int original = result.Count;
            for (int i = 0; i < original; ++i)
            {
                var subset = new List<int>(result[i]);
                subset.Add(value);
                result.Add(subset);
            }
        }
        return result;
    }
}
