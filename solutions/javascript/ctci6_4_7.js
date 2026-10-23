'use strict';
function BuildOrder(projectCount, dependencies) {
  const adjacent = Array.from({ length: projectCount }, () => []),
    indegree = new Array(projectCount).fill(0),
    order = [];
  for (const [before, after] of dependencies) {
    adjacent[before].push(after);
    ++indegree[after];
  }
  for (let i = 0; i < projectCount; ++i) if (indegree[i] === 0) order.push(i);
  for (let head = 0; head < order.length; ++head)
    for (const dependent of adjacent[order[head]]) {
      --indegree[dependent];
      if (indegree[dependent] === 0) order.push(dependent);
    }
  return order.length === projectCount ? order : [];
}

module.exports = {BuildOrder};
