using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public int[] MajorityElement(int[] values)
    {
        int candidate = 0, balance = 0;
        foreach (int value in values)
        {
            if (balance == 0)
                candidate = value;
            balance += value == candidate ? 1 : -1;
        }
        int count = 0;
        foreach (int value in values)
        {
            if (value == candidate)
                ++count;
        }
        if (count > values.Length / 2)
            return [candidate];
        return [];
    }
}
