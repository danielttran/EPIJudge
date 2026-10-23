using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public double[] SegmentIntersection(int[][] endpoints)
    {
        int[] a = endpoints[0], b = endpoints[1], c = endpoints[2], d = endpoints[3];
        int rx = b[0] - a[0], ry = b[1] - a[1], sx = d[0] - c[0], sy = d[1] - c[1],
            qx = c[0] - a[0], qy = c[1] - a[1], denominator = rx * sy - ry * sx;
        if (denominator != 0)
        {
            int first = qx * sy - qy * sx, second = qx * ry - qy * rx;
            if (denominator < 0)
            {
                denominator = -denominator;
                first = -first;
                second = -second;
            }
            if (first >= 0 && first <= denominator && second >= 0 && second <= denominator)
            {
                double t = (double)first / denominator;
                return [a[0] + t * rx, a[1] + t * ry];
            }
            return [];
        }
        bool Contains(int[] start, int[] end, int[] point)
        {
            return (end[0] - start[0]) * (point[1] - start[1]) ==
                       (end[1] - start[1]) * (point[0] - start[0]) &&
                   point[0] >= Math.Min(start[0], end[0]) &&
                   point[0] <= Math.Max(start[0], end[0]) &&
                   point[1] >= Math.Min(start[1], end[1]) && point[1] <= Math.Max(start[1], end[1]);
        }
        foreach (var point in endpoints)
            if (Contains(a, b, point) && Contains(c, d, point))
                return [(double)point[0], (double)point[1]];
        return [];
    }
}
