using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public List<string> EliminateDuplicate(List<(string, string)> names)
    {
        var distinct = new HashSet<string>(StringComparer.Ordinal);
        foreach (var name in names)
            distinct.Add(name.Item1);
        return distinct.ToList();
    }
}
