using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public int NumCombinationsForFinalScore(int final_score, List<int> individual_play_scores)
    {
        int[] ways = new int[final_score + 1];
        ways[0] = 1;
        foreach (int score in individual_play_scores)
            for (int total = score; total <= final_score; total++)
                ways[total] += ways[total - score];
        return ways[final_score];
    }
}
