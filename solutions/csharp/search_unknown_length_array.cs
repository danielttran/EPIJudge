using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public int BinarySearchUnknownLength(List<int> A, int k)
    {
        bool Read(int index, out int value)
        {
            try
            {
                value = A[index];
                return true;
            }
            catch (ArgumentOutOfRangeException) { value = 0; return false; }
        }
        int left = 0, right = 1;
        while (Read(right, out int value) && value < k)
        {
            left = right + 1;
            if (right > (int.MaxValue - 1) / 2)
            {
                right = int.MaxValue;
                break;
            }
            right = 2 * right + 1;
        }
        while (left <= right)
        {
            int middle = left + (right - left) / 2;
            if (!Read(middle, out int value) || value > k)
                right = middle - 1;
            else if (value < k)
                left = middle + 1;
            else
                return middle;
        }
        return -1;
    }
}
