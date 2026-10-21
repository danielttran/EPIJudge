using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public List<(int, double)> CalculateTrafficVolumes(List<(int, double)> A, int w)
    {
        var candidates = new LinkedList<int>();
        var result = new List<(int, double)>();
        for (int i = 0; i < A.Count; i++)
        {
            while (candidates.Count > 0 && (long)A[candidates.First!.Value].Item1 < (long)A[i].Item1 - w)
                candidates.RemoveFirst();
            while (candidates.Count > 0 && A[candidates.Last!.Value].Item2 <= A[i].Item2)
                candidates.RemoveLast();
            candidates.AddLast(i);
            result.Add((A[i].Item1, A[candidates.First!.Value].Item2));
        }
        return result;
    }
}
