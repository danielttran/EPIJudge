using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public int FindLineWithMostPoints(List<(int, int)> points)
    {
        int answer = 0;
        static long Gcd(long a, long b)
        {
            while (b != 0)
                (a, b) = (b, a % b);
            return a;
        }
        for (int i = 0; i < points.Count; i++)
        {
            var counts = new Dictionary<(long, long), int>();
            int duplicates = 1, best = 0;
            for (int j = i + 1; j < points.Count; j++)
            {
                long dx = (long)points[j].Item1 - points[i].Item1;
                long dy = (long)points[j].Item2 - points[i].Item2;
                if (dx == 0 && dy == 0)
                {
                    duplicates++;
                    continue;
                }
                long divisor = Gcd(Math.Abs(dx), Math.Abs(dy));
                dx /= divisor;
                dy /= divisor;
                if (dx < 0 || (dx == 0 && dy < 0))
                {
                    dx = -dx;
                    dy = -dy;
                }
                var slope = (dx, dy);
                counts.TryGetValue(slope, out int count);
                counts[slope] = ++count;
                best = Math.Max(best, count);
            }
            answer = Math.Max(answer, best + duplicates);
        }
        return answer;
    }
}
