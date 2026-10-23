using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public int AddWithoutArithmetic(int first, int second)
    {
        uint a = unchecked((uint)first), b = unchecked((uint)second);
        while (b != 0)
        {
            uint carry = (a & b) << 1;
            a ^= b;
            b = carry;
        }
        return unchecked((int)a);
    }
}
