using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public int SearchEntryEqualToItsIndex(List<int> values)
    {
        int left = 0, right = values.Count - 1;
        while (left <= right)
        {
            int middle = left + (right - left) / 2;
            long difference = (long)values[middle] - middle;
            if (difference == 0)
                return middle;
            if (difference < 0)
                left = middle + 1;
            else
                right = middle - 1;
        }
        return -1;
    }
}
