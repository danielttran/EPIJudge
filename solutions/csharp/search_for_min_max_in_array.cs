using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public (int, int) FindMinMax(List<int> A)
    {
        if (A.Count == 0)
            throw new ArgumentException("A nonempty array is required.");
        int minimum, maximum, next;
        if ((A.Count & 1) != 0)
        {
            minimum = maximum = A[0];
            next = 1;
        }
        else
        {
            (minimum, maximum) = A[0] < A[1] ? (A[0], A[1]) : (A[1], A[0]);
            next = 2;
        }
        for (int i = next; i < A.Count; i += 2)
        {
            int low, high;
            if (A[i] < A[i + 1])
            {
                low = A[i];
                high = A[i + 1];
            }
            else
            {
                low = A[i + 1];
                high = A[i];
            }
            if (low < minimum)
                minimum = low;
            if (high > maximum)
                maximum = high;
        }
        return (minimum, maximum);
    }
}
