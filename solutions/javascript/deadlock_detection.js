function isDeadlocked(num_nodes, edges) {
  const graph = Array.from({ length: num_nodes }, () => []),
    indegree = Array(num_nodes).fill(0),
    ready = [];
  for (const [from, to] of edges) {
    graph[from].push(to);
    indegree[to]++;
  }
  for (let v = 0; v < num_nodes; v++) if (!indegree[v]) ready.push(v);
  for (let head = 0; head < ready.length; head++)
    for (const neighbor of graph[ready[head]])
      if (--indegree[neighbor] === 0) ready.push(neighbor);
  return ready.length !== num_nodes;
}

module.exports = { isDeadlocked };
