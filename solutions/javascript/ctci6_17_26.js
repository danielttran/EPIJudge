'use strict';
function SparseSimilarities(documentIds, documents) {
  const n = documentIds.length,
    postings = new Map(),
    intersections = new Map();
  for (let i = 0; i < n; ++i)
    for (const word of documents[i]) {
      if (!postings.has(word)) postings.set(word, []);
      postings.get(word).push(i);
    }
  for (const posting of postings.values())
    for (let left = 0; left < posting.length; ++left)
      for (let right = left + 1; right < posting.length; ++right) {
        const key = posting[left] * n + posting[right];
        intersections.set(key, (intersections.get(key) || 0) + 1);
      }
  const result = [];
  for (const [key, count] of intersections) {
    const left = Math.floor(key / n),
      right = key % n,
      a = documentIds[left],
      b = documentIds[right];
    result.push([
      Math.min(a, b),
      Math.max(a, b),
      count,
      documents[left].length + documents[right].length - count,
    ]);
  }
  result.sort((a, b) => a[0] - b[0] || a[1] - b[1]);
  return result;
}

module.exports = {SparseSimilarities};
