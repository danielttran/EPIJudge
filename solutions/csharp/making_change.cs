using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public int ChangeMaking(int cents)
    {
        int result = 0;
        foreach (int coin in new[] { 100, 50, 25, 10, 5, 1 })
        {
            result += cents / coin;
            cents %= coin;
        }
        return result;
    }
}
