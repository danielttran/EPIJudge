using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public int[] LongestLettersDigits(string text)
    {
        int n = text.Length;
        int[] first = new int[2 * n + 1];
        Array.Fill(first, -2);
        first[n] = -1;
        int balance = 0, best = 0, start = -1, end = -1;
        for (int i = 0; i < n; ++i)
        {
            balance += (text[i] >= '0' && text[i] <= '9') ? -1 : 1;
            int slot = balance + n;
            if (first[slot] == -2)
                first[slot] = i;
            else if (i - first[slot] > best)
            {
                best = i - first[slot];
                start = first[slot] + 1;
                end = i;
            }
        }
        return [start, end];
    }
}
