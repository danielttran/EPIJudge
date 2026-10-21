using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public List<int> DeleteDuplicates(List<int> A)
    {
        var result = new List<int>();
        foreach (int value in A)
        if (result.Count == 0 || result[^1] != value)
            result.Add(value);
        return result;
    }
}
