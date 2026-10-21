using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public int MinimumMessiness(List<string> words, int line_length)
    {
        var best = new int[words.Count + 1];
        for (int end = 1; end <= words.Count; end++)
        {
            best[end] = int.MaxValue;
            int used = 0;
            for (int start = end - 1; start >= 0; start--)
            {
                used += words[start].Length + (start == end - 1 ? 0 : 1);
                if (used > line_length)
                    break;
                int spaces = line_length - used;
                if (best[start] != int.MaxValue)
                    best[end] = Math.Min(best[end], best[start] + spaces * spaces);
            }
        }
        return best[^1];
    }
}
