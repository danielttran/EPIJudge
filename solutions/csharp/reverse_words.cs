using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public string ReverseWords(string s)
    {
        char[] text = s.ToCharArray();
        Array.Reverse(text);
        int start = 0;
        while (start < text.Length)
        {
            if (text[start] == ' ')
            {
                start++;
                continue;
            }
            int end = start;
            while (end < text.Length && text[end] != ' ')
                end++;
            Array.Reverse(text, start, end - start);
            start = end;
        }
        return new string(text);
    }
}
