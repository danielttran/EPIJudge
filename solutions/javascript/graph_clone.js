function cloneGraph(graph) {
  const copies = new Map([[graph, new GraphVertex(graph.label)]]),
    pending = [graph];
  for (let head = 0; head < pending.length; head++) {
    const original = pending[head];
    for (const neighbor of original.edges) {
      if (!copies.has(neighbor)) {
        copies.set(neighbor, new GraphVertex(neighbor.label));
        pending.push(neighbor);
      }
      copies.get(original).edges.push(copies.get(neighbor));
    }
  }
  return copies.get(graph);
}

module.exports = { cloneGraph };
