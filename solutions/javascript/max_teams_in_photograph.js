function findLargestNumberTeams(k, edges) {
  const outgoing = Array.from({ length: k }, () => []),
    incoming = Array(k).fill(0),
    length = Array(k).fill(1),
    ready = [];
  for (const [from, to] of edges) {
    outgoing[from].push(to);
    incoming[to]++;
  }
  for (let i = 0; i < k; i++) if (incoming[i] === 0) ready.push(i);
  let best = 0;
  for (let head = 0; head < ready.length; head++) {
    const team = ready[head];
    best = Math.max(best, length[team]);
    for (const next of outgoing[team]) {
      length[next] = Math.max(length[next], length[team] + 1);
      if (--incoming[next] === 0) ready.push(next);
    }
  }
  return best;
}

module.exports = { findLargestNumberTeams };
