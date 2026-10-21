using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public List<List<string>> PalindromeDecompositions(string text)
    {
        int n = text.Length;
        var palindrome = new bool[n, n];
        for (int start = n - 1; start >= 0; start--)
            for (int end = start; end < n; end++)
                palindrome[start, end] = text[start] == text[end] && (end - start < 2 || palindrome[start + 1, end - 1]);
        var result = new List<List<string>>();
        var parts = new List<string>();
        void Search(int start)
        {
            if (start == n)
            {
                result.Add(new List<string>(parts));
                return;
            }
            for (int end = start; end < n; end++)
                if (palindrome[start, end])
                {
                    parts.Add(text[start..(end + 1)]);
                    Search(end + 1);
                    parts.RemoveAt(parts.Count - 1);
                }
        }
        Search(0);
        return result;
    }
}
