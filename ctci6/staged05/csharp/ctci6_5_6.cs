using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public int CountBitChanges(int first, int second)
    {
        uint difference = unchecked((uint)(first ^ second));
        int count = 0;
        while (difference != 0)
        {
            difference &= difference - 1;
            ++count;
        }
        return count;
    }
}
