using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public List<int> RotateArray(List<int> A, int rotate_amount)
    {
        if (A.Count == 0)
            return A;
        int amount = rotate_amount % A.Count;
        if (amount < 0)
            amount += A.Count;
        A.Reverse();
        A.Reverse(0, amount);
        A.Reverse(amount, A.Count - amount);
        return A;
    }
}
