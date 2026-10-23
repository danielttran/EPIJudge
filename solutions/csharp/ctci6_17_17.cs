using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public int[][] MultiSearch(string text, string[] patterns)
    {
        var result = new List<int[]>();
        foreach (string pattern in patterns)
        {
            var positions = new List<int>();
            for (int start = 0; start + pattern.Length <= text.Length; ++start)
                if (string.CompareOrdinal(text, start, pattern, 0, pattern.Length) == 0)
                    positions.Add(start);
            result.Add(positions.ToArray());
        }
        return result.ToArray();
    }
}
