using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public int[] ShortestCoveringRange(int[] big, int[] small)
    {
        if (small.Length == 0)
            return [-1, -1];
        var counts = new Dictionary<int, int>();
        foreach (int value in small)
            counts[value] = 0;
        int missing = small.Length, left = 0, start = -1, end = -1;
        for (int right = 0; right < big.Length; ++right)
        {
            int value = big[right];
            if (counts.ContainsKey(value))
            {
                if (counts[value] == 0)
                    --missing;
                ++counts[value];
            }
            while (missing == 0)
            {
                if (start == -1 || right - left < end - start)
                {
                    start = left;
                    end = right;
                }
                int removed = big[left];
                if (counts.ContainsKey(removed))
                {
                    --counts[removed];
                    if (counts[removed] == 0)
                        ++missing;
                }
                ++left;
            }
        }
        return [start, end];
    }
}
