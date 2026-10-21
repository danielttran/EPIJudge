using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public int LevenshteinDistance(string A, string B)
    {
        if (B.Length > A.Length)
            return LevenshteinDistance(B, A);
        int[] previous = Enumerable.Range(0, B.Length + 1).ToArray();
        for (int i = 1; i <= A.Length; i++)
        {
            int[] current = new int[B.Length + 1];
            current[0] = i;
            for (int j = 1; j <= B.Length; j++)
                current[j] = A[i - 1] == B[j - 1] ? previous[j - 1] : 1 + Math.Min(previous[j - 1], Math.Min(previous[j], current[j - 1]));
            previous = current;
        }
        return previous[B.Length];
    }
}
