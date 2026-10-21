using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public List<int> ApplyPermutation(List<int> perm, List<int> A)
    {
        var result = Enumerable.Repeat(0, A.Count).ToList();
        for (int i = 0; i < A.Count; i++)
            result[perm[i]] = A[i];
        return result;
    }
}
