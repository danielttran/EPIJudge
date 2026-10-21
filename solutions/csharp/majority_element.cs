using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public string MajoritySearch(List<string> stream)
    {
        string candidate = "";
        int balance = 0;
        foreach (string value in stream)
        {
            if (balance == 0)
                candidate = value;
            balance += value == candidate ? 1 : -1;
        }
        return candidate;
    }
}
