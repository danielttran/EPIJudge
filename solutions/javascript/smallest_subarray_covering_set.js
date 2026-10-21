function findSmallestSubarrayCoveringSet(paragraph, keywords) {
  keywords = new Set(keywords);
  if (!keywords.size) return [0, -1];
  const counts = new Map();
  let present = 0,
    left = 0,
    bestLength = Infinity,
    best = [-1, -1];
  for (let right = 0; right < paragraph.length; right++) {
    const word = paragraph[right];
    if (keywords.has(word)) {
      const count = counts.get(word) || 0;
      if (!count) present++;
      counts.set(word, count + 1);
    }
    while (present === keywords.size && left <= right) {
      if (right - left + 1 < bestLength) {
        best = [left, right];
        bestLength = right - left + 1;
      }
      const removed = paragraph[left++];
      if (keywords.has(removed)) {
        counts.set(removed, counts.get(removed) - 1);
        if (!counts.get(removed)) present--;
      }
    }
  }
  return best;
}

module.exports = { findSmallestSubarrayCoveringSet };
