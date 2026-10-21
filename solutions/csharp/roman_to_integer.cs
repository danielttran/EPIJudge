using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public int RomanToInteger(string s)
    {
        int Value(char c) => c switch
        {
            'I' => 1,
            'V' => 5,
            'X' => 10,
            'L' => 50,
            'C' => 100,
            'D' => 500,
            'M' => 1000,
            _ => throw new ArgumentException("Unknown symbol")
        };
        int total = 0;
        for (int i = 0; i < s.Length; i++)
        {
            int current = Value(s[i]);
            total += i + 1 < s.Length && current < Value(s[i + 1]) ? -current : current;
        }
        return total;
    }
}
