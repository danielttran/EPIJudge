using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public int MinimumTotalWaitingTime(List<int> service_times)
    {
        int waiting = 0, elapsed = 0;
        foreach (int duration in service_times.Order())
        {
            waiting += elapsed;
            elapsed += duration;
        }
        return waiting;
    }
}
