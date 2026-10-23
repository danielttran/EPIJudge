import java.util.*;
class Solution {
  public double[] SegmentIntersection(int[][] endpoints) {
    int[] a = endpoints[0], b = endpoints[1], c = endpoints[2], d = endpoints[3];
    int rx = b[0] - a[0], ry = b[1] - a[1], sx = d[0] - c[0], sy = d[1] - c[1], qx = c[0] - a[0],
        qy = c[1] - a[1], denominator = rx * sy - ry * sx;
    if (denominator != 0) {
      int first = qx * sy - qy * sx, second = qx * ry - qy * rx;
      if (denominator < 0) {
        denominator = -denominator;
        first = -first;
        second = -second;
      }
      if (first >= 0 && first <= denominator && second >= 0 && second <= denominator) {
        double t = (double) first / denominator;
        return new double[] {a[0] + t * rx, a[1] + t * ry};
      }
      return new double[0];
    }
    class Geometry {
      boolean contains(int[] start, int[] end, int[] point) {
        return (end[0] - start[0]) * (point[1] - start[1])
            == (end[1] - start[1]) * (point[0] - start[0])
            && point[0] >= Math.min(start[0], end[0]) && point[0] <= Math.max(start[0], end[0])
            && point[1] >= Math.min(start[1], end[1]) && point[1] <= Math.max(start[1], end[1]);
      }
    }
    var geometry = new Geometry();
    for (int[] point : endpoints)
      if (geometry.contains(a, b, point) && geometry.contains(c, d, point))
        return new double[] {(double) point[0], (double) point[1]};
    return new double[0];
  }
}
