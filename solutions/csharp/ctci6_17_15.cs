using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public string LongestComposedWord(string[] words)
    {
        var dictionary = new HashSet<string>(words, StringComparer.Ordinal);
        string best = "";
        foreach (string word in words)
        {
            int[] dp = new int[word.Length + 1];
            Array.Fill(dp, -1);
            dp[0] = 0;
            for (int end = 1; end <= word.Length; ++end)
                for (int start = 0; start < end; ++start)
                    if (dp[start] >= 0 && dictionary.Contains(word.Substring(start, end - start)))
                        dp[end] = Math.Max(dp[end], dp[start] + 1);
            if (dp[word.Length] >= 2 &&
                (word.Length > best.Length ||
                 (word.Length == best.Length && StringComparer.Ordinal.Compare(word, best) < 0)))
                best = word;
        }
        return best;
    }
}
