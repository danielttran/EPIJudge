'use strict';
function WordFrequencies(book, queries) {
  const counts = new Map();
  for (const word of book) {
    const key = word.toLowerCase();
    counts.set(key, (counts.get(key) || 0) + 1);
  }
  return queries.map((word) => counts.get(word.toLowerCase()) || 0);
}
