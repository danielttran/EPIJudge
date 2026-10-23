using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public int SwapAdjacentBits(int word)
    {
        uint bits = unchecked((uint)word);
        uint result = ((bits & 0x55555555u) << 1) | ((bits & 0xaaaaaaaau) >> 1);
        return unchecked((int)result);
    }
}
