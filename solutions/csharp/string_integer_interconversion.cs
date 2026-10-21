using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public string IntToString(int value)
    {
        bool negative = value < 0;
        long remaining = negative ? -(long)value : value;
        var reversed = new List<char>();
        do
        {
            reversed.Add((char)('0' + remaining % 10));
            remaining /= 10;
        } while (remaining > 0);
        if (negative)
            reversed.Add('-');
        reversed.Reverse();
        return new string(reversed.ToArray());
    }
    public int StringToInt(string text)
    {
        int index = 0;
        bool negative = false;
        if (text.Length > 0 && (text[0] == '-' || text[0] == '+'))
        {
            negative = text[0] == '-';
            index++;
        }
        long value = 0;
        for (; index < text.Length; index++)
            value = checked(value * 10 + text[index] - '0');
        return checked((int)(negative ? -value : value));
    }
}
