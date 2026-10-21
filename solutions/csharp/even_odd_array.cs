using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public void EvenOdd(List<int> values)
    {
        int even = 0, unknown = 0;
        while (unknown < values.Count)
        {
            if ((values[unknown] & 1) == 0)
            {
                (values[even], values[unknown]) = (values[unknown], values[even]);
                even++;
            }
            unknown++;
        }
    }
}
