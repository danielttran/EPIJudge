using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public bool HasTwoSum(List<int> values, int target)
    {
        int left = 0, right = values.Count - 1;
        while (left <= right)
        {
            long sum = (long)values[left] + values[right];
            if (sum == target)
                return true;
            if (sum < target)
                left++;
            else
                right--;
        }
        return false;
    }
}
