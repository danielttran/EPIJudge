function findAllSubstrings(s, words) {
  const result = [];
  if (!words.length || !words[0].length) return result;
  const width = words[0].length,
    required = new Map();
  for (const word of words) required.set(word, (required.get(word) || 0) + 1);
  for (let offset = 0; offset < width; offset++) {
    let seen = new Map(),
      left = offset,
      count = 0;
    for (let right = offset; right + width <= s.length; right += width) {
      const word = s.slice(right, right + width);
      if (!required.has(word)) {
        seen = new Map();
        count = 0;
        left = right + width;
        continue;
      }
      seen.set(word, (seen.get(word) || 0) + 1);
      count++;
      while (seen.get(word) > required.get(word)) {
        const removed = s.slice(left, left + width);
        seen.set(removed, seen.get(removed) - 1);
        left += width;
        count--;
      }
      if (count === words.length) {
        result.push(left);
        const removed = s.slice(left, left + width);
        seen.set(removed, seen.get(removed) - 1);
        left += width;
        count--;
      }
    }
  }
  return result.sort((a, b) => a - b);
}

module.exports = { findAllSubstrings };
