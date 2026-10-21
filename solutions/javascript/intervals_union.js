function unionOfIntervals(intervals) {
  const ordered = intervals
      .slice()
      .sort((a, b) => a[0] - b[0] || Number(b[1]) - Number(a[1])),
    result = [];
  for (const next of ordered) {
    if (!result.length) {
      result.push(next.slice());
      continue;
    }
    let current = result.at(-1);
    const overlaps =
      next[0] < current[2] ||
      (next[0] === current[2] && (current[3] || next[1]));
    if (!overlaps) {
      result.push(next.slice());
      continue;
    }
    const leftClosed = current[1] || (next[0] === current[0] && next[1]);
    if (next[2] > current[2])
      current = [current[0], leftClosed, next[2], next[3]];
    else if (next[2] === current[2])
      current = [current[0], leftClosed, current[2], current[3] || next[3]];
    else current = [current[0], leftClosed, current[2], current[3]];
    result[result.length - 1] = current;
  }
  return result;
}

module.exports = { unionOfIntervals };
