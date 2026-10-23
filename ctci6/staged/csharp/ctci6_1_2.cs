using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public bool CheckPermutation(string first, string second)
    {
        if (first.Length != second.Length)
            return false;
        int[] counts = new int[128];
        for (int i = 0; i < first.Length; ++i)
            ++counts[first[i]];
        for (int i = 0; i < second.Length; ++i)
        {
            int code = second[i];
            --counts[code];
            if (counts[code] < 0)
                return false;
        }
        return true;
    }
}
