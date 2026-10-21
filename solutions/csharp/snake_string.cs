using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public string SnakeString(string s)
    {
        var output = new System.Text.StringBuilder(s.Length);
        for (int i = 1; i < s.Length; i += 4)
            output.Append(s[i]);
        for (int i = 0; i < s.Length; i += 2)
            output.Append(s[i]);
        for (int i = 3; i < s.Length; i += 4)
            output.Append(s[i]);
        return output.ToString();
    }
}
