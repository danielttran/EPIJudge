using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public int LongestNondecreasingSubsequenceLength(List<int> A)
    {
        var tails = new List<int>();
        foreach (int value in A)
        {
            int low = 0, high = tails.Count;
            while (low < high)
            {
                int mid = low + (high - low) / 2;
                if (tails[mid] <= value)
                    low = mid + 1;
                else
                    high = mid;
            }
            if (low == tails.Count)
                tails.Add(value);
            else
                tails[low] = value;
        }
        return tails.Count;
    }
}
