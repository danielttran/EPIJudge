using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public int RabinKarp(string t, string s)
    {
        if (s.Length == 0)
            return 0;
        if (s.Length > t.Length)
            return -1;
        const ulong radix = 65599;
        ulong pattern = 0, window = 0, power = 1;
        unchecked
        {
            for (int i = 0; i < s.Length; i++)
            {
                pattern = pattern * radix + s[i];
                window = window * radix + t[i];
                if (i > 0)
                    power *= radix;
            }
            for (int start = 0; ; start++)
            {
                if (window == pattern && t.AsSpan(start, s.Length).SequenceEqual(s.AsSpan()))
                    return start;
                if (start + s.Length == t.Length)
                    return -1;
                window = (window - (ulong)t[start] * power) * radix + t[start + s.Length];
            }
        }
    }
}
