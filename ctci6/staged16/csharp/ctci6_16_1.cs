using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public int[] SwapWithoutTemporary(int first, int second)
    {
        first ^= second;
        second ^= first;
        first ^= second;
        return [first, second];
    }
}
