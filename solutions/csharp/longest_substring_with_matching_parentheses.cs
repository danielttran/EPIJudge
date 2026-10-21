using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public int LongestMatchingParentheses(string s)
    {
        var openings = new Stack<int>();
        openings.Push(-1);
        int best = 0;
        for (int i = 0; i < s.Length; i++)
        {
            if (s[i] == '(')
                openings.Push(i);
            else
            {
                openings.Pop();
                if (openings.Count == 0)
                    openings.Push(i);
                else
                    best = Math.Max(best, i - openings.Peek());
            }
        }
        return best;
    }
}
