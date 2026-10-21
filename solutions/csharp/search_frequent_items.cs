using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public List<string> SearchFrequentItems(int k, List<string> stream)
    {
        var counts = new Dictionary<string, int>(StringComparer.Ordinal);
        foreach (string item in stream)
            counts[item] = counts.GetValueOrDefault(item) + 1;
        return counts.Where(pair => (long)pair.Value * k > stream.Count)
                     .Select(pair => pair.Key).ToList();
    }
}
