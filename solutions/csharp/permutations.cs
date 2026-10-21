using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public List<List<int>> Permutations(List<int> A)
    {
        var result = new List<List<int>>();
        void Visit(int first)
        {
            if (first == A.Count)
            {
                result.Add(new List<int>(A));
                return;
            }
            for (int i = first; i < A.Count; i++)
            {
                (A[first], A[i]) = (A[i], A[first]);
                Visit(first + 1);
                (A[first], A[i]) = (A[i], A[first]);
            }
        }
        Visit(0);
        return result;
    }
}
