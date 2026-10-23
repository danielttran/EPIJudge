using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public long SmallestDifference(int[] first, int[] second)
    {
        if (first.Length == 0 || second.Length == 0)
            return -1;
        int[] a = (int[])first.Clone(), b = (int[])second.Clone();
        Array.Sort(a);
        Array.Sort(b);
        int i = 0, j = 0;
        long best = 4294967295L;
        while (i < a.Length && j < b.Length)
        {
            long difference = (long)a[i] - b[j];
            best = Math.Min(best, Math.Abs(difference));
            if (difference == 0)
                return 0;
            if (difference < 0)
                ++i;
            else
                ++j;
        }
        return best;
    }
}
