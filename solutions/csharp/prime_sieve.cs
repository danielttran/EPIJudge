using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public List<int> GeneratePrimes(int n)
    {
        var primes = new List<int>();
        if (n < 2)
            return primes;
        var composite = new bool[n + 1];
        for (int p = 2; p <= n; p++)
        {
            if (composite[p])
                continue;
            primes.Add(p);
            if ((long)p * p > n)
                continue;
            for (long multiple = (long)p * p; multiple <= n; multiple += p)
                composite[(int)multiple] = true;
        }
        return primes;
    }
}
