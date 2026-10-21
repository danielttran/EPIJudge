using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public bool HasThreeSum(List<int> A, int t)
    {
        var values = A.Order().ToList();
        foreach (int first in values)
        {
            int left = 0, right = values.Count - 1;
            while (left <= right)
            {
                long sum = (long)first + values[left] + values[right];
                if (sum == t)
                    return true;
                if (sum < t)
                    left++;
                else
                    right--;
            }
        }
        return false;
    }
}
