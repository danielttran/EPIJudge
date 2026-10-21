function searchFrequentItems(k, stream) {
  const counts = new Map();
  for (const item of stream) counts.set(item, (counts.get(item) || 0) + 1);
  return [...counts]
    .filter(([, count]) => count * k > stream.length)
    .map(([item]) => item);
}

module.exports = { searchFrequentItems };
