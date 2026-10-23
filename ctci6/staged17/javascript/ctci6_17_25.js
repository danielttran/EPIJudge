'use strict';
function LargestWordRectangle(words) {
  const groups = new Map(),
    seen = new Set();
  let maximum = 0;
  for (const word of words)
    if (!seen.has(word)) {
      seen.add(word);
      if (!groups.has(word.length)) groups.set(word.length, []);
      groups.get(word.length).push(word);
      maximum = Math.max(maximum, word.length);
    }
  for (let area = maximum * maximum; area > 0; --area)
    for (let height = 1; height <= maximum; ++height) {
      if (area % height !== 0) continue;
      const width = area / height;
      if (!groups.has(width) || !groups.has(height)) continue;
      const prefixes = new Set();
      for (const word of groups.get(height))
        for (let length = 1; length <= height; ++length) prefixes.add(word.slice(0, length));
      const rows = [];
      function search() {
        if (rows.length === height) return true;
        for (const word of groups.get(width)) {
          rows.push(word);
          let valid = true;
          for (let column = 0; column < width; ++column) {
            let prefix = "";
            for (const row of rows) prefix += row[column];
            if (!prefixes.has(prefix)) {
              valid = false;
              break;
            }
          }
          if (valid && search()) return true;
          rows.pop();
        }
        return false;
      }
      if (search()) return rows;
    }
  return [];
}
