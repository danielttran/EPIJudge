using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public int UniformRandom(int lower, int upper)
    {
        ulong range = (ulong)((long)upper - lower + 1);
        int bits = 0;
        for (ulong remaining = range - 1; remaining > 0; remaining >>= 1)
            bits++;
        ulong candidate;
        do
        {
            candidate = 0;
            for (int i = 0; i < bits; i++)
                candidate = (candidate << 1) | (uint)Random.Shared.Next(2);
        } while (candidate >= range);
        return (int)((long)lower + (long)candidate);
    }
}
