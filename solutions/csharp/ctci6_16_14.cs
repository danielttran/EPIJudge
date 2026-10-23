using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public int[] BestLine(int[][] points)
    {
        if (points.Length == 0)
            return [];
        int Gcd(int a, int b)
        {
            while (b != 0)
            {
                int next = a % b;
                a = b;
                b = next;
            }
            return a;
        }
        int[] best = [1, 0,
                      -points [0]
                      [0]];
        int bestCount = 0;
        for (int anchor = 0; anchor < points.Length; ++anchor)
        {
            var groups = new Dictionary<(int Dy, int Dx), int>();
            int duplicates = 0, x = points[anchor][0], y = points[anchor][1];
            for (int other = anchor + 1; other < points.Length; ++other)
            {
                int dx = points[other][0] - x, dy = points[other][1] - y;
                if (dx == 0 && dy == 0)
                {
                    ++duplicates;
                    continue;
                }
                int divisor = Gcd(Math.Abs(dx), Math.Abs(dy));
                dx /= divisor;
                dy /= divisor;
                if (dx < 0 || (dx == 0 && dy < 0))
                {
                    dx = -dx;
                    dy = -dy;
                }
                groups.TryGetValue((dy, dx), out int count);
                groups[(dy, dx)] = count + 1;
            }
            foreach (var entry in groups)
                if (entry.Value + duplicates + 1 > bestCount)
                {
                    bestCount = entry.Value + duplicates + 1;
                    int a = entry.Key.Dy, b = -entry.Key.Dx, c = -a * x - b * y;
                    if (a < 0 || (a == 0 && b < 0))
                    {
                        a = -a;
                        b = -b;
                        c = -c;
                    }
                    best = [a, b, c];
                }
        }
        return best;
    }
}
