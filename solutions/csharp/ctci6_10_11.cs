using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public int[] ArrangePeaksValleys(int[] values)
    {
        for (int i = 1; i < values.Length; i += 2)
        {
            int best = i;
            if (values[i - 1] > values[best])
                best = i - 1;
            if (i + 1 < values.Length && values[i + 1] > values[best])
                best = i + 1;
            int temporary = values[i];
            values[i] = values[best];
            values[best] = temporary;
        }
        return values;
    }
}
