using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public int RecursiveMultiply(int first, int second)
    {
        int smaller = Math.Min(first, second), larger = Math.Max(first, second);
        if (smaller == 0)
            return 0;
        int half = RecursiveMultiply(smaller >> 1, larger);
        return half + half + ((smaller & 1) != 0 ? larger : 0);
    }
}
