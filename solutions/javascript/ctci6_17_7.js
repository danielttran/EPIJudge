'use strict';
function TrueNameFrequencies(names, frequencies, synonyms) {
  const adjacent = Array.from({ length: names.length }, () => []),
    visited = new Array(names.length).fill(false),
    result = [];
  for (const [first, second] of synonyms) {
    adjacent[first].push(second);
    adjacent[second].push(first);
  }
  for (let start = 0; start < names.length; ++start) {
    if (visited[start]) continue;
    visited[start] = true;
    const queue = [start];
    let total = 0;
    for (let head = 0; head < queue.length; ++head) {
      const name = queue[head];
      total += frequencies[name];
      for (const other of adjacent[name])
        if (!visited[other]) {
          visited[other] = true;
          queue.push(other);
        }
    }
    result.push([start, total]);
  }
  return result;
}

module.exports = {TrueNameFrequencies};
