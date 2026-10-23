'use strict';
function BestLine(points) {
  if (points.length === 0) return [];
  function gcd(a, b) {
    while (b !== 0) {
      const next = a % b;
      a = b;
      b = next;
    }
    return a;
  }
  let best = [1, 0, -points[0][0]],
    bestCount = 0;
  for (let anchor = 0; anchor < points.length; ++anchor) {
    const groups = new Map(),
      [x, y] = points[anchor];
    let duplicates = 0;
    for (let other = anchor + 1; other < points.length; ++other) {
      let dx = points[other][0] - x,
        dy = points[other][1] - y;
      if (dx === 0 && dy === 0) {
        ++duplicates;
        continue;
      }
      const divisor = gcd(Math.abs(dx), Math.abs(dy));
      dx /= divisor;
      dy /= divisor;
      if (dx < 0 || (dx === 0 && dy < 0)) {
        dx = -dx;
        dy = -dy;
      }
      const key = dy + "," + dx;
      groups.set(key, (groups.get(key) || 0) + 1);
    }
    for (const [key, count] of groups)
      if (count + duplicates + 1 > bestCount) {
        bestCount = count + duplicates + 1;
        const [dy, dx] = key.split(",").map(Number);
        let a = dy,
          b = -dx,
          c = -a * x - b * y;
        if (a < 0 || (a === 0 && b < 0)) {
          a = -a;
          b = -b;
          c = -c;
        }
        best = [a, b, c];
      }
  }
  return best;
}

module.exports = {BestLine};
