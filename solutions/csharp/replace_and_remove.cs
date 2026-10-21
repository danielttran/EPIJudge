using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public List<string> ReplaceAndRemove(int size, List<string> s)
    {
        var result = new List<string>();
        for (int i = 0; i < size; i++)
        {
            if (s[i] == "a")
            {
                result.Add("d");
                result.Add("d");
            }
            else if (s[i] != "b")
                result.Add(s[i]);
        }
        return result;
    }
}
