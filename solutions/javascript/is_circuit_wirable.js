function isAnyPlacementFeasible(k, edges) {
  const neighbors = Array.from({ length: k }, () => []),
    colors = Array(k).fill(-1);
  for (const [a, b] of edges) {
    neighbors[a].push(b);
    neighbors[b].push(a);
  }
  for (let start = 0; start < k; start++) {
    if (colors[start] !== -1) continue;
    colors[start] = 0;
    const queue = [start];
    for (let head = 0; head < queue.length; head++) {
      const node = queue[head];
      for (const next of neighbors[node]) {
        if (colors[next] === colors[node]) return false;
        if (colors[next] !== -1) continue;
        colors[next] = 1 - colors[node];
        queue.push(next);
      }
    }
  }
  return true;
}

module.exports = { isAnyPlacementFeasible };
