using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public int[] RepeatedOccurrences(int[] values)
    {
        byte[] bits = new byte[4000];
        int count = 0;
        foreach (int value in values)
        {
            int slot = (value - 1) >> 3, mask = 1 << ((value - 1) & 7);
            if ((bits[slot] & mask) != 0)
                ++count;
            else
                bits[slot] = (byte)(bits[slot] | mask);
        }
        int[] result = new int[count];
        Array.Clear(bits);
        int write = 0;
        foreach (int value in values)
        {
            int slot = (value - 1) >> 3, mask = 1 << ((value - 1) & 7);
            if ((bits[slot] & mask) != 0)
                result[write++] = value;
            else
                bits[slot] = (byte)(bits[slot] | mask);
        }
        return result;
    }
}
