function findLineWithMostPoints(points) {
  let answer = 0;
  function gcd(a, b) {
    while (b) [a, b] = [b, a % b];
    return a;
  }
  for (let i = 0; i < points.length; i++) {
    const counts = new Map();
    let duplicates = 1,
      best = 0;
    for (let j = i + 1; j < points.length; j++) {
      let dx = points[j][0] - points[i][0],
        dy = points[j][1] - points[i][1];
      if (dx === 0 && dy === 0) {
        duplicates++;
        continue;
      }
      const divisor = gcd(Math.abs(dx), Math.abs(dy));
      dx /= divisor;
      dy /= divisor;
      if (dx < 0 || (dx === 0 && dy < 0)) {
        dx = -dx;
        dy = -dy;
      }
      const slope = dx + "," + dy,
        count = (counts.get(slope) || 0) + 1;
      counts.set(slope, count);
      best = Math.max(best, count);
    }
    answer = Math.max(answer, best + duplicates);
  }
  return answer;
}

module.exports = { findLineWithMostPoints };
