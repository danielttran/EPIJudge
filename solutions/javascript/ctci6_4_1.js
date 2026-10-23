'use strict';
function HasDirectedRoute(nodeCount, edges, start, target) {
  if (start === target) return true;
  const adjacent = Array.from({ length: nodeCount }, () => []),
    visited = new Array(nodeCount).fill(false),
    queue = [start];
  for (const [source, destination] of edges) adjacent[source].push(destination);
  visited[start] = true;
  for (let head = 0; head < queue.length; ++head)
    for (const neighbor of adjacent[queue[head]])
      if (!visited[neighbor]) {
        if (neighbor === target) return true;
        visited[neighbor] = true;
        queue.push(neighbor);
      }
  return false;
}

module.exports = {HasDirectedRoute};
