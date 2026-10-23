using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public int SearchRotated(int[] values, int target)
    {
        int left = 0, right = values.Length - 1;
        while (left <= right)
        {
            int middle = left + (right - left) / 2;
            if (values[middle] == target)
                return middle;
            if (values[left] == values[middle] && values[middle] == values[right])
            {
                ++left;
                --right;
            }
            else if (values[left] <= values[middle])
            {
                if (values[left] <= target && target < values[middle])
                    right = middle - 1;
                else
                    left = middle + 1;
            }
            else
            {
                if (values[middle] < target && target <= values[right])
                    left = middle + 1;
                else
                    right = middle - 1;
            }
        }
        return -1;
    }
}
