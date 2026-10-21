using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public void DutchFlagPartition(int pivotIndex, List<int> values)
    {
        int pivot = values[pivotIndex];
        int smaller = 0, current = 0, larger = values.Count;
        while (current < larger)
        {
            if (values[current] < pivot)
            {
                (values[smaller], values[current]) = (values[current], values[smaller]);
                smaller++;
                current++;
            }
            else if (values[current] == pivot)
                current++;
            else
            {
                larger--;
                (values[current], values[larger]) = (values[larger], values[current]);
            }
        }
    }
}
