function minimumMessiness(words, line_length) {
  const best = Array(words.length + 1).fill(Infinity);
  best[0] = 0;
  for (let end = 1; end <= words.length; end++) {
    let used = 0;
    for (let start = end - 1; start >= 0; start--) {
      used += words[start].length + (start === end - 1 ? 0 : 1);
      if (used > line_length) break;
      best[end] = Math.min(best[end], best[start] + (line_length - used) ** 2);
    }
  }
  return best[words.length];
}

module.exports = { minimumMessiness };
