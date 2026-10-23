using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public int[][] PairsWithSum(int[] values, int target)
    {
        int[] ordered = (int[])values.Clone();
        Array.Sort(ordered);
        var result = new List<int[]>();
        int left = 0, right = ordered.Length - 1;
        while (left < right)
        {
            long total = (long)ordered[left] + ordered[right];
            if (total == target)
            {
                result.Add([ordered[left], ordered[right]]);
                ++left;
                --right;
            }
            else if (total < target)
                ++left;
            else
                --right;
        }
        return result.ToArray();
    }
}
