function findSmallestSequentiallyCoveringSubset(paragraph, keywords) {
  if (!keywords.length) return [0, -1];
  const positions = new Map(keywords.map((word, index) => [word, index])),
    start = Array(keywords.length).fill(-1);
  let best = [-1, -1],
    bestLength = Infinity;
  for (let i = 0; i < paragraph.length; i++) {
    if (!positions.has(paragraph[i])) continue;
    const p = positions.get(paragraph[i]);
    if (p === 0) start[0] = i;
    else if (start[p - 1] >= 0) start[p] = start[p - 1];
    if (
      p === keywords.length - 1 &&
      start[p] >= 0 &&
      i - start[p] + 1 < bestLength
    ) {
      best = [start[p], i];
      bestLength = i - start[p] + 1;
    }
  }
  return best;
}

module.exports = { findSmallestSequentiallyCoveringSubset };
