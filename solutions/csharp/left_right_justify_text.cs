using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public List<string> JustifyText(List<string> words, int L)
    {
        var result = new List<string>();
        for (int first = 0; first < words.Count;)
        {
            int end = first + 1, letters = words[first].Length;
            while (end < words.Count && letters + words[end].Length + end - first <= L)
                letters += words[end++].Length;
            int gaps = end - first - 1;
            var line = new System.Text.StringBuilder();
            for (int i = first; i < end; i++)
            {
                line.Append(words[i]);
                if (i + 1 < end)
                {
                    int spaces = end == words.Count ? 1 : (L - letters) / gaps + (i - first < (L - letters) % gaps ? 1 : 0);
                    line.Append(' ', spaces);
                }
            }
            line.Append(' ', L - line.Length);
            result.Add(line.ToString());
            first = end;
        }
        return result;
    }
}
