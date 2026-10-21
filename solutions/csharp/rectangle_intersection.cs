using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public (int, int, int, int) IntersectRectangle((int, int, int, int) r1, (int, int, int, int) r2)
    {
        int left = Math.Max(r1.Item1, r2.Item1);
        int bottom = Math.Max(r1.Item2, r2.Item2);
        long right = Math.Min((long)r1.Item1 + r1.Item3, (long)r2.Item1 + r2.Item3);
        long top = Math.Min((long)r1.Item2 + r1.Item4, (long)r2.Item2 + r2.Item4);
        return left > right || bottom > top ? (0, 0, -1, -1) : (left, bottom, (int)(right - left), (int)(top - bottom));
    }
}
