using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public (int Start, int End) FindSmallestSequentiallyCoveringSubset(List<string> paragraph, List<string> keywords)
    {
        if (keywords.Count == 0)
            return (0, -1);
        var positions = keywords.Select((word, index) => (word, index)).ToDictionary(x => x.word, x => x.index);
        var start = Enumerable.Repeat(-1, keywords.Count).ToArray();
        var best = (-1, -1);
        int bestLength = int.MaxValue;
        for (int i = 0; i < paragraph.Count; i++)
        {
            if (!positions.TryGetValue(paragraph[i], out int position))
                continue;
            if (position == 0)
                start[0] = i;
            else if (start[position - 1] >= 0)
                start[position] = start[position - 1];
            if (position == keywords.Count - 1 && start[position] >= 0 && i - start[position] + 1 < bestLength)
            {
                best = (start[position], i);
                bestLength = i - start[position] + 1;
            }
        }
        return best;
    }
}
