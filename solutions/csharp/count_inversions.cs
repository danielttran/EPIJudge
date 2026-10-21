using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public int CountInversions(List<int> A)
    {
        var values = A.ToArray();
        var temporary = new int[values.Length];
        int Sort(int start, int end)
        {
            if (end - start <= 1)
                return 0;
            int middle = start + (end - start) / 2;
            int count = Sort(start, middle) + Sort(middle, end);
            int i = start, j = middle, outIndex = start;
            while (i < middle || j < end)
            {
                if (j == end || (i < middle && values[i] <= values[j]))
                    temporary[outIndex++] = values[i++];
                else
                {
                    temporary[outIndex++] = values[j++];
                    count += middle - i;
                }
            }
            Array.Copy(temporary, start, values, start, end - start);
            return count;
        }
        return Sort(0, values.Length);
    }
}
