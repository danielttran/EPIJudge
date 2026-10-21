using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public List<List<string>> FindAnagrams(List<string> dictionary)
    {
        var groups = new Dictionary<string, List<string>>();
        foreach (string word in dictionary)
        {
            string key = new string(word.OrderBy(c => c).ToArray());
            if (!groups.TryGetValue(key, out var group))
                groups[key] = group = [];
            group.Add(word);
        }
        return groups.Values.Where(group => group.Count > 1).ToList();
    }
}
