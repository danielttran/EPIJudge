using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public List<int> NextPermutation(List<int> perm)
    {
        int pivot = perm.Count - 2;
        while (pivot >= 0 && perm[pivot] >= perm[pivot + 1])
            pivot--;
        if (pivot < 0)
            return new List<int>();
        int successor = perm.Count - 1;
        while (perm[successor] <= perm[pivot])
            successor--;
        (perm[pivot], perm[successor]) = (perm[successor], perm[pivot]);
        for (int left = pivot + 1, right = perm.Count - 1; left < right; left++, right--)
            (perm[left], perm[right]) = (perm[right], perm[left]);
        return perm;
    }
}
