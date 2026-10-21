using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public List<List<int>> Combinations(int n, int k)
    {
        var result = new List<List<int>>();
        var chosen = new List<int>();
        void Search(int next)
        {
            if (chosen.Count == k)
            {
                result.Add(new List<int>(chosen));
                return;
            }
            int needed = k - chosen.Count;
            for (int value = next; value <= n - needed + 1; value++)
            {
                chosen.Add(value);
                Search(value + 1);
                chosen.RemoveAt(chosen.Count - 1);
            }
        }
        if (k >= 0 && k <= n)
            Search(1);
        return result;
    }
}
