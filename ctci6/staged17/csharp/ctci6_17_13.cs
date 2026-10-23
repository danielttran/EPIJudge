using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public List<string> ReSpace(string text, string[] dictionary)
    {
        var words = new HashSet<string>(dictionary, StringComparer.Ordinal);
        int maximum = 0;
        foreach (string word in words)
            maximum = Math.Max(maximum, word.Length);
        int[] cost = new int[text.Length + 1], previous = new int[text.Length + 1];
        for (int end = 1; end <= text.Length; ++end)
        {
            cost[end] = cost[end - 1] + 1;
            previous[end] = end - 1;
            for (int length = 1; length <= maximum && length <= end; ++length)
            {
                int start = end - length;
                if (words.Contains(text.Substring(start, length)) && cost[start] < cost[end])
                {
                    cost[end] = cost[start];
                    previous[end] = start;
                }
            }
        }
        var result = new List<string>();
        for (int end = text.Length; end > 0; end = previous[end])
            result.Add(text.Substring(previous[end], end - previous[end]));
        result.Reverse();
        return result;
    }
}
