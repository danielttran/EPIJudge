using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public List<double> GenerateFirstKABSqrt2(int k)
    {
        if (k <= 0)
            return [];
        var pairs = new List<(int A, int B)> { (0, 0) };
        var result = new List<double> { 0 };
        int plusOne = 0, plusRoot = 0;
        double root = Math.Sqrt(2);
        while (result.Count < k)
        {
            var first = (A: pairs[plusOne].A + 1, B: pairs[plusOne].B);
            var second = (A: pairs[plusRoot].A, B: pairs[plusRoot].B + 1);
            double x = first.A + first.B * root, y = second.A + second.B * root;
            var next = x <= y ? first : second;
            pairs.Add(next);
            result.Add(next.A + next.B * root);
            if (first == next)
                plusOne++;
            if (second == next)
                plusRoot++;
        }
        return result;
    }
}
