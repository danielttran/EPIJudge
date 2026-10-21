using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public string Encoding(string text)
    {
        var output = new System.Text.StringBuilder();
        for (int start = 0; start < text.Length;)
        {
            int end = start + 1;
            while (end < text.Length && text[end] == text[start])
                end++;
            output.Append(end - start).Append(text[start]);
            start = end;
        }
        return output.ToString();
    }
    public string Decoding(string encoded)
    {
        var output = new System.Text.StringBuilder();
        int count = 0;
        foreach (char c in encoded)
        {
            if (c >= '0' && c <= '9')
                count = count * 10 + c - '0';
            else
            {
                output.Append(c, count);
                count = 0;
            }
        }
        return output.ToString();
    }
}
