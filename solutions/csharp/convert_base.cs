using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public string ConvertBase(string num_as_string, int b1, int b2)
    {
        const string digits = "0123456789ABCDEF";
        bool negative = num_as_string.StartsWith('-');
        System.Numerics.BigInteger value = 0;
        foreach (char c in num_as_string.AsSpan(negative ? 1 : 0))
            value = value * b1 + digits.IndexOf(char.ToUpperInvariant(c));
        if (value.IsZero)
            return "0";
        var result = new List<char>();
        while (value > 0)
        {
            result.Add(digits[(int)(value % b2)]);
            value /= b2;
        }
        if (negative)
            result.Add('-');
        result.Reverse();
        return new string(result.ToArray());
    }
}
