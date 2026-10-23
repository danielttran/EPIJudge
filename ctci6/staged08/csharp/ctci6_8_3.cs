using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public int FindMagicIndex(int[] values, bool distinctValues)
    {
        if (distinctValues)
        {
            int low = 0, high = values.Length - 1;
            while (low <= high)
            {
                int middle = low + (high - low) / 2;
                if (values[middle] == middle)
                    return middle;
                if (values[middle] > middle)
                    high = middle - 1;
                else
                    low = middle + 1;
            }
            return -1;
        }
        int Search(int low, int high)
        {
            if (low > high)
                return -1;
            int middle = low + (high - low) / 2, value = values[middle];
            if (value == middle)
                return middle;
            int left = Search(low, Math.Min(middle - 1, value));
            return left != -1 ? left : Search(Math.Max(middle + 1, value), high);
        }
        return Search(0, values.Length - 1);
    }
}
