using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public List<string> GenerateBalancedParentheses(int num_pairs)
    {
        var result = new List<string>();
        var buffer = new char[2 * num_pairs];
        void Search(int opened, int closed)
        {
            int position = opened + closed;
            if (position == buffer.Length)
            {
                result.Add(new string(buffer));
                return;
            }
            if (opened < num_pairs)
            {
                buffer[position] = '(';
                Search(opened + 1, closed);
            }
            if (closed < opened)
            {
                buffer[position] = ')';
                Search(opened, closed + 1);
            }
        }
        Search(0, 0);
        return result;
    }
}
