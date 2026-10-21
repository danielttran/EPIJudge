using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public int SsDecodeColId(string col)
    {
        int value = 0;
        foreach (char c in col)
            value = checked(value * 26 + (c - 'A' + 1));
        return value;
    }
}
