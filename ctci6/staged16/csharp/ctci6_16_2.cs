using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public int[] WordFrequencies(string[] book, string[] queries)
    {
        var counts = new Dictionary<string, int>(StringComparer.Ordinal);
        foreach (string word in book)
        {
            string key = word.ToLowerInvariant();
            counts.TryGetValue(key, out int count);
            counts[key] = count + 1;
        }
        int[] result = new int[queries.Length];
        for (int i = 0; i < queries.Length; ++i)
        {
            counts.TryGetValue(queries[i].ToLowerInvariant(), out int count);
            result[i] = count;
        }
        return result;
    }
}
