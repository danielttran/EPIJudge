using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public List<int> FindAllSubstrings(string s, List<string> words)
    {
        var result = new List<int>();
        if (words.Count == 0 || words[0].Length == 0)
            return result;
        int width = words[0].Length;
        var required = new Dictionary<string, int>();
        foreach (string word in words)
            required[word] = required.GetValueOrDefault(word) + 1;
        for (int offset = 0; offset < width; offset++)
        {
            var seen = new Dictionary<string, int>();
            int left = offset, count = 0;
            for (int right = offset; right + width <= s.Length; right += width)
            {
                string word = s.Substring(right, width);
                if (!required.ContainsKey(word))
                {
                    seen = new Dictionary<string, int>();
                    count = 0;
                    left = right + width;
                    continue;
                }
                seen[word] = seen.GetValueOrDefault(word) + 1;
                count++;
                while (seen[word] > required[word])
                {
                    string removed = s.Substring(left, width);
                    seen[removed]--;
                    left += width;
                    count--;
                }
                if (count == words.Count)
                {
                    result.Add(left);
                    string removed = s.Substring(left, width);
                    seen[removed]--;
                    left += width;
                    count--;
                }
            }
        }
        result.Sort();
        return result;
    }
}
