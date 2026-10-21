function findNearestRepetition(paragraph) {
  const last = new Map();
  let best = Infinity;
  for (let i = 0; i < paragraph.length; i++) {
    if (last.has(paragraph[i]))
      best = Math.min(best, i - last.get(paragraph[i]));
    last.set(paragraph[i], i);
  }
  return best === Infinity ? -1 : best;
}

module.exports = { findNearestRepetition };
