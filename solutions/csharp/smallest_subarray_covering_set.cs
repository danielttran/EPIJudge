using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public (int Start, int End) FindSmallestSubarrayCoveringSet(List<string> paragraph, HashSet<string> keywords)
    {
        if (keywords.Count == 0)
            return (0, -1);
        var counts = new Dictionary<string, int>();
        int present = 0, left = 0, bestLength = int.MaxValue;
        var best = (-1, -1);
        for (int right = 0; right < paragraph.Count; right++)
        {
            string word = paragraph[right];
            if (keywords.Contains(word))
            {
                int count = counts.GetValueOrDefault(word);
                if (count == 0)
                    present++;
                counts[word] = count + 1;
            }
            while (present == keywords.Count && left <= right)
            {
                if (right - left + 1 < bestLength)
                {
                    best = (left, right);
                    bestLength = right - left + 1;
                }
                string removed = paragraph[left++];
                if (keywords.Contains(removed) && --counts[removed] == 0)
                    present--;
            }
        }
        return best;
    }
}
