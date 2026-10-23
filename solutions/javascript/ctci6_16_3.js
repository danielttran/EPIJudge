'use strict';
function SegmentIntersection(endpoints) {
  const [a, b, c, d] = endpoints,
    rx = b[0] - a[0],
    ry = b[1] - a[1],
    sx = d[0] - c[0],
    sy = d[1] - c[1],
    qx = c[0] - a[0],
    qy = c[1] - a[1];
  let denominator = rx * sy - ry * sx;
  if (denominator !== 0) {
    let first = qx * sy - qy * sx,
      second = qx * ry - qy * rx;
    if (denominator < 0) {
      denominator = -denominator;
      first = -first;
      second = -second;
    }
    if (first >= 0 && first <= denominator && second >= 0 && second <= denominator) {
      const t = first / denominator;
      return [a[0] + t * rx, a[1] + t * ry];
    }
    return [];
  }
  function contains(start, end, point) {
    return (
      (end[0] - start[0]) * (point[1] - start[1]) === (end[1] - start[1]) * (point[0] - start[0]) &&
      point[0] >= Math.min(start[0], end[0]) &&
      point[0] <= Math.max(start[0], end[0]) &&
      point[1] >= Math.min(start[1], end[1]) &&
      point[1] <= Math.max(start[1], end[1])
    );
  }
  for (const point of endpoints)
    if (contains(a, b, point) && contains(c, d, point)) return [point[0], point[1]];
  return [];
}

module.exports = {SegmentIntersection};
