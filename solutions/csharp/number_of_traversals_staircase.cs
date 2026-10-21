using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public int NumberOfWaysToTop(int top, int maximum_step)
    {
        if (maximum_step <= 0)
            return top == 0 ? 1 : 0;
        int[] ways = new int[top + 1];
        ways[0] = 1;
        long window = 1;
        for (int stair = 1; stair <= top; stair++)
        {
            ways[stair] = (int)window;
            window += ways[stair];
            if (stair >= maximum_step)
                window -= ways[stair - maximum_step];
        }
        return ways[top];
    }
}
