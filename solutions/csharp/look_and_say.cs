using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public string LookAndSay(int n)
    {
        string term = "1";
        for (int step = 1; step < n; step++)
        {
            var next = new System.Text.StringBuilder();
            for (int first = 0; first < term.Length;)
            {
                int end = first + 1;
                while (end < term.Length && term[end] == term[first])
                    end++;
                next.Append(end - first).Append(term[first]);
                first = end;
            }
            term = next.ToString();
        }
        return term;
    }
}
