function justifyText(words, L) {
  const result = [];
  for (let first = 0; first < words.length; ) {
    let end = first + 1,
      letters = words[first].length;
    while (end < words.length && letters + words[end].length + end - first <= L)
      letters += words[end++].length;
    const gaps = end - first - 1,
      parts = [];
    let length = 0;
    for (let i = first; i < end; i++) {
      parts.push(words[i]);
      length += words[i].length;
      if (i + 1 < end) {
        const spaces =
          end === words.length
            ? 1
            : Math.floor((L - letters) / gaps) +
              (i - first < (L - letters) % gaps ? 1 : 0);
        parts.push(" ".repeat(spaces));
        length += spaces;
      }
    }
    parts.push(" ".repeat(L - length));
    result.push(parts.join(""));
    first = end;
  }
  return result;
}

module.exports = { justifyText };
