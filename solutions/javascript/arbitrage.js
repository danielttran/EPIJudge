function isArbitrageExist(graph) {
  const n = graph.length,
    distances = Array(n).fill(0);
  for (let pass = 0; pass < n; pass++) {
    let changed = false;
    for (let from = 0; from < n; from++)
      for (let to = 0; to < n; to++) {
        const candidate = distances[from] - Math.log(graph[from][to]);
        if (candidate < distances[to] - 1e-12) {
          distances[to] = candidate;
          changed = true;
        }
      }
    if (!changed) return false;
  }
  return true;
}

module.exports = { isArbitrageExist };
