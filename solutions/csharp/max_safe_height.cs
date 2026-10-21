using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public int GetHeight(int cases, int drops)
    {
        cases = Math.Min(cases, drops);
        int[] covered = new int[cases + 1];
        for (int test = 0; test < drops; test++)
            for (int eggs = cases; eggs > 0; eggs--)
                covered[eggs] = (int)Math.Min(int.MaxValue, 1L + covered[eggs] + covered[eggs - 1]);
        return covered[cases];
    }
}
