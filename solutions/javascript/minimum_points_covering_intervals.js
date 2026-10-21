function findMinimumVisits(A) {
  let visits = 0,
    last = -Infinity;
  for (const interval of A.slice().sort((a, b) => a[1] - b[1]))
    if (interval[0] > last) {
      visits++;
      last = interval[1];
    }
  return visits;
}

module.exports = { findMinimumVisits };
